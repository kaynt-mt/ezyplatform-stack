# Young Monkeys: supporting projects and when to use them

These are options for extending the MVP later, not required dependencies. The [inventory](index.md) links to individual articles.

## Integration and configuration

- [EzyMQ](https://youngmonkeys.org/projects/ezymq?lang=vi) has guides for Kafka, RabbitMQ, ActiveMQ, and Mosquitto, covering transport configuration, producers, consumers, topics, and examples. The Overview currently repeats the Quick RPC description, so use the Guides to classify it. The [push example](https://youngmonkeys.org/ezymq/guides/use-ezykafka-for-push-message-system?lang=vi) separates ingress and delivery: client → EzyHTTP → Kafka → EzyFox Server → client. For durable delivery, write the outbox entry in the same transaction; a broker is not necessary at first. If you add one, check retries and deduplication, ordering by business key, replay, and authorization before fan-out. The example does not provide those guarantees for the plugin.
- [Quick RPC](https://youngmonkeys.org/quickrpc/guides/introduce-quick-rpc?lang=vi) separates the server that registers handlers from the client that sends requests. Use it only across actual service boundaries, not between a controller and SDK in the same runtime. If a worker is split into its own service, define service-to-service authentication, timeouts, payload versions, and idempotency. Do not use example credentials.
- [EzyFox Boot](https://youngmonkeys.org/projects/ezyfox-boot?lang=vi) describes auto-configuration and provides samples for JPA, MongoDB, and Redis, but the index lists no separate guide. It can help with a standalone Java worker. A plugin uses the host's context rather than bootstrapping its own stack.
- [Properties File](https://youngmonkeys.org/projects/properties-file?lang=vi) reads YAML and `.properties`, supports profiles, and explains value encryption. Keep configuration small and prefer the runtime's existing configuration and secret injection. Keep decryption keys separate from the data and ZIP. Encrypting values does not replace secret management or rotation.

## Patterns not to copy directly into plugins

- [Game Box](https://youngmonkeys.org/projects/game-box?lang=vi) models players, rooms, and position synchronization. It is useful for understanding delivery to a set of recipients, but room state does not replace durable ACLs, revocation, or auditing. Add the dependency only if you need game features.
- [Test Utilities](https://youngmonkeys.org/projects/test-utilities?lang=vi) covers TestNG and Mockito assertions, exceptions, sample data, reflection, and timing. Unit-test state transitions and policies. Use startup and integration tests on the target SDK and MySQL to check transactions, SQL, HTTP binding, and authentication. Mocks cannot prove mappings or rollbacks. Control concurrency test data and seeds, and do not treat small timing examples as SLAs.
