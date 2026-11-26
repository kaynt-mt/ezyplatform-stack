#!/usr/bin/env python3
import argparse
import http.cookiejar
import json
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zipfile import BadZipFile, ZipFile

EZY = Path(__file__).resolve().with_name("ezy")
PROJECT_NAME = re.compile(r"[a-z][a-z0-9-]{1,59}")
UPLOAD_PROJECT_NAME = re.compile(r"[a-z0-9][a-z0-9-]{1,59}")
JAVA_NAME = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+")
MODULE_TYPES = {"admin-plugin", "web-plugin", "theme", "socket-plugin", "socket-app"}
CORE_JAR = re.compile(
    r"ezyplatform-(?:(?:admin|common|socket|web)(?:-sdk)?|devtools|http-sdk|test-sdk|sdk)-[0-9][^/]*\.jar",
    re.IGNORECASE,
)


def fix_assembly_exclusions(assembly, group):
    content = assembly.read_text(encoding="utf-8")
    corrected = re.sub(
        r"(<exclude>\s*)" + re.escape(group) + r"(:ezyplatform-[\w.-]+\s*</exclude>)",
        r"\g<1>org.youngmonkeys\2",
        content,
    )
    if corrected != content:
        assembly.write_text(corrected, encoding="utf-8")


def create_project(name, native_options, group, package, modules, output):
    if not PROJECT_NAME.fullmatch(name):
        raise ValueError("Project name must be 2–60 lowercase letters, digits or hyphens and start with a letter")
    if not JAVA_NAME.fullmatch(group) or not JAVA_NAME.fullmatch(package):
        raise ValueError("Group and package must be dotted lowercase Java names, such as com.example")
    module_types = modules.split(",")
    if len(set(module_types)) != len(module_types) or not set(module_types) <= MODULE_TYPES:
        raise ValueError("Choose unique module types from: " + ", ".join(sorted(MODULE_TYPES)))

    output = output.resolve()
    project = output / name
    try:
        project.mkdir(parents=True)
    except FileExistsError as error:
        raise ValueError(f"Project path already exists: {project}") from error

    try:
        subprocess.run(
            [str(EZY), "dev", "run", *native_options, "--", "ezy.sh", "create", name,
             "-g", group, "-p", package, "-i", modules, "-o", str(output)],
            input="yes\n",
            text=True,
            check=True,
        )
        if not (project / "pom.xml").is_file():
            raise ValueError("SDK did not generate the project POM")
        for module in module_types:
            assembly = project / f"{name}-{module}" / "assembly.xml"
            fix_assembly_exclusions(assembly, group)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        try:
            project.rmdir()
        except OSError:
            pass
        raise ValueError(f"Scaffold failed; inspect any files left in {project}: {error}") from error
    return project


def check_zip(path):
    with ZipFile(path) as archive:
        entries = archive.namelist()
        if not entries:
            raise ValueError("Project ZIP is empty")
        bundled = [
            name for name in entries
            if CORE_JAR.fullmatch(name.replace("\\", "/").rsplit("/", 1)[-1])
        ]
        if bundled:
            raise ValueError("Project ZIP bundles EzyPlatform core JARs: " + ", ".join(bundled))
        damaged = archive.testzip()
        if damaged:
            raise ValueError(f"Project ZIP contains a corrupt entry: {damaged}")


def open_admin_session(admin_url, username, password):
    parsed = urllib.parse.urlparse(admin_url)
    loopback = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    if parsed.scheme != "https" and not loopback:
        raise ValueError("Remote Admin URLs must use HTTPS; plain HTTP is allowed only on loopback")
    cookies = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
    body = urllib.parse.urlencode({"username": username, "password": password}).encode()
    request = urllib.request.Request(admin_url.rstrip("/") + "/login", data=body, method="POST")
    with opener.open(request, timeout=30) as response:
        if response.status >= 400:
            raise ValueError(f"Admin login failed with HTTP {response.status}")
    return opener


def admin_request(opener, admin_url, path, method="GET", data=None, headers=None):
    request = urllib.request.Request(
        admin_url.rstrip("/") + path,
        data=data,
        headers=headers or {},
        method=method,
    )
    try:
        with opener.open(request, timeout=60) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        raise ValueError(f"{method} {path} failed with HTTP {error.code}: {body[:300]}") from error


def upload_project_zip(opener, admin_url, zip_path):
    boundary = "----ezy-plugin-upload-boundary"
    content = zip_path.read_bytes()
    body = b"".join((
        ("--" + boundary + "\r\n").encode(),
        (
            'Content-Disposition: form-data; name="file"; filename="' +
            zip_path.name + '"\r\n'
        ).encode(),
        b"Content-Type: application/zip\r\n\r\n",
        content,
        ("\r\n--" + boundary + "--\r\n").encode(),
    ))
    return admin_request(
        opener,
        admin_url,
        "/api/v1/projects/upload",
        "POST",
        body,
        {"Content-Type": "multipart/form-data; boundary=" + boundary},
    )


def upload_and_apply_zip(admin_url, username, password, zip_path):
    check_zip(zip_path)
    opener = open_admin_session(admin_url, username, password)
    _, status_body = admin_request(opener, admin_url, "/api/v1/projects/version-status")
    projects = json.loads(status_body)
    if not isinstance(projects, list) or not all(isinstance(project, dict) for project in projects):
        raise ValueError("Admin did not return valid project version status")

    upload_status, upload_body = upload_project_zip(opener, admin_url, zip_path)
    upload_response = json.loads(upload_body or "{}")
    project_name = upload_response.get("projectName") if isinstance(upload_response, dict) else None
    if not isinstance(project_name, str) or not UPLOAD_PROJECT_NAME.fullmatch(project_name):
        raise ValueError("Project upload did not return a valid projectName")

    check_status, _ = admin_request(opener, admin_url, "/api/v1/projects/check-dependencies")
    project_path = f"/api/v1/projects/{project_name}"
    result = {
        "upload_status": upload_status,
        "upload_response": upload_response,
        "check_dependencies_status": check_status,
    }
    if any(project.get("projectName") == project_name and project.get("status") == "INSTALLED"
           for project in projects):
        result["platform_install_status"], _ = admin_request(
            opener, admin_url, "/api/v1/platform/install", "POST", b""
        )
        return result

    _, types_body = admin_request(opener, admin_url, f"{project_path}/module-types")
    module_types = json.loads(types_body)
    if not isinstance(module_types, list) or not module_types or not all(
        isinstance(kind, str) and kind in MODULE_TYPES for kind in module_types
    ):
        raise ValueError(f"Project {project_name} did not return valid module types")
    activation_status, _ = admin_request(
        opener, admin_url, f"{project_path}/activate", "POST",
        json.dumps({"moduleTypes": module_types, "restart": True}).encode(),
        {"Content-Type": "application/json"},
    )
    return dict(result, activation_status=activation_status, module_types=module_types)


def main():
    parser = argparse.ArgumentParser(description="Scaffold an EzyPlatform project or check its exported ZIP")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="Scaffold into a new project directory")
    create.add_argument("name")
    native = create.add_mutually_exclusive_group(required=True)
    native.add_argument("--dir", type=Path, help="Root created by the native install skill")
    native.add_argument("--home", type=Path, help="Standalone native runtime containing cli.sh")
    create.add_argument("--group", required=True)
    create.add_argument("--package", required=True)
    create.add_argument("--modules", default="admin-plugin,web-plugin")
    create.add_argument("--out", type=Path, required=True)
    check = commands.add_parser("check-zip", help="Check ZIP integrity and reject bundled core JARs")
    check.add_argument("zip", type=Path)
    upload = commands.add_parser(
        "upload-apply",
        help="Upload a checked ZIP to Docker dev Admin and activate or apply it",
    )
    upload.add_argument("zip", type=Path)
    upload.add_argument("--admin-url", default="http://127.0.0.1:9090")
    upload.add_argument("--username", default="admin")
    upload.add_argument("--password-file", type=Path, required=True)
    args = parser.parse_args()

    try:
        if args.command == "create":
            native_options = ["--dir", str(args.dir.resolve())] if args.dir else ["--home", str(args.home.resolve())]
            project = create_project(args.name, native_options, args.group, args.package, args.modules, args.out)
            print(f"Project created: {project}")
        elif args.command == "check-zip":
            check_zip(args.zip)
            print(f"ZIP passed integrity and core JAR checks: {args.zip}")
        else:
            password = args.password_file.read_text(encoding="utf-8").rstrip("\r\n")
            result = upload_and_apply_zip(
                args.admin_url, args.username, password, args.zip
            )
            print(json.dumps(result, indent=2, sort_keys=True))
            action = ("Uploaded and activated; restart requested."
                      if "activation_status" in result else "Uploaded and applied.")
            print(
                f"{action} Poll the installed module version, route registrations, "
                "migration schema, and plugin-specific smoke routes before declaring success."
            )
    except (OSError, ValueError, BadZipFile) as error:
        parser.exit(1, f"ezy-plugin: {error}\n")


if __name__ == "__main__":
    main()
