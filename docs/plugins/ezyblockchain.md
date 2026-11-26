# ezyblockchain

Chain, token và quản lý địa chỉ ví.

- **Bản Marketplace trên core 1.5.9:** `0.0.3`.
- **Module đã xác minh:** `admin-plugin`, `web-plugin`.
- **Cài đặt:** Đạt qua Admin. Xem môi trường và các giới hạn chung trong [báo cáo kiểm thử](test-report.md).

## Bản đồ module

| Lane / thư mục | Package khai báo | Phụ thuộc runtime khai báo |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyblockchain` | `org.youngmonkeys.ezyblockchain` | Không khai báo |
| `web-plugin` — `web/plugins/ezyblockchain` | `org.youngmonkeys.ezyblockchain` | Không khai báo |

## HTTP, UI và tài nguyên

Các đường dẫn dưới đây đến từ annotation trong JAR. Tiền tố khi mount module và quyền truy cập có thể khác giữa các lane; các URL đã gọi thật nằm ở mục kiểm thử.

**admin-plugin** — 16 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /chains` | `ChainController` |
| `GET /control-panel` | `ControlPanelController` |
| `GET /chains/add` | `ChainController` |
| `GET /ezyblockchain/api/v1/admins/me/wallet-addresses` | `ApiAdminController` |
| `GET /chains/{chainId}` | `ChainController` |
| `GET /chains/{chainId}/edit` | `ChainController` |
| `GET /api/v1/{chainId}/latest-block-height` | `ApiBlockController` |
| `POST /api/v1/chains/add` | `ApiChainController` |
| `POST /ezyblockchain/api/v1/admins/me/link-wallet-address` | `ApiAdminController` |
| `POST /api/v1/{chainId}/processors/stop` | `ApiProcessingController` |
| `POST /api/v1/{chainId}/processors/start` | `ApiProcessingController` |
| `PUT /api/v1/chains/{chainId}` | `ApiChainController` |
| `PUT /api/v1/chains/{chainId}/set-as-current` | `ApiChainController` |
| `DELETE /api/v1/chains/{chainId}` | `ApiChainController` |

**web-plugin** — 11 tổ hợp phương thức/URI đọc được; mẫu đại diện:

| Annotation HTTP | Class |
|---|---|
| `GET /ezyblockchain/api/v1/chains/current` | `ApiChainController` |
| `GET /ezyblockchain/api/v1/users/me/wallet-addresses` | `ApiUserController` |
| `GET /ezyblockchain/api/v1/chains/{chainId}` | `ApiChainController` |
| `GET /ezyblockchain/api/v1/chains/{chainId}/blocks` | `ApiBlockController` |
| `GET /ezyblockchain/api/v1/chains/{chainId}/accounts` | `ApiAccountController` |
| `GET /ezyblockchain/api/v1/chains/{chainId}/contracts` | `ApiContractController` |
| `GET /ezyblockchain/api/v1/chains/{chainId}/transactions` | `ApiTransactionController` |
| `POST /ezyblockchain/api/v1/users/me/link-wallet-address` | `ApiUserController` |

- **admin-plugin – Menu (khóa cuối và path trong menus.properties):** `ezyblockchain: /`, `control_panel: /control-panel`, `chain_list: /chains`, `add_chain: ~/chains/add`, `edit_chain: ~/chains/{chainId}/edit`, `chain_details: ~/chains/{chainId}`.

- **admin-plugin – Template:** `ezyblockchain/chains/add.html`, `ezyblockchain/chains/details.html`, `ezyblockchain/chains/edit.html`, `ezyblockchain/chains/list.html`, `ezyblockchain/chains/scripts.html`, `ezyblockchain/control-panel/index.html`.

## Dữ liệu và migration

- **Bảng trong DDL đóng gói (9):** `ezyblockchain_address_transactions`, `ezyblockchain_addresses`, `ezyblockchain_blocks`, `ezyblockchain_chains`, `ezyblockchain_nfts`, `ezyblockchain_processed_block_height`, `ezyblockchain_processing_block_height`, `ezyblockchain_transactions`, `ezyblockchain_transfers`.
- **Class có chỉ dấu JPA Entity/MappedSuperclass (9):** `BAddress`, `BAddressTransaction`, `BBlock`, `BChain`, `BNft`, `BProcessedBlockHeight`, `BProcessingBlockHeight`, `BTransaction`, `BTransfer`.
- **SQL admin-plugin (2 tệp):** `resources/scripts/scripts.sql`, `resources/scripts/alter_tables_1.sql`.

## JAR, cấu hình và điểm mở rộng

### admin-plugin

- **JAR kiểm tra:** `ezyblockchain-admin-plugin-0.0.3.jar`, `ezyblockchain-sdk-0.0.3.jar`; 178 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyblockchain.pagination`, `org.youngmonkeys.ezyblockchain.entity`, `org.youngmonkeys.ezyblockchain.model` (+32).
- **JAR thư viện khác:** `Java-WebSocket-1.3.8.jar`, `abi-5.0.0.jar`, `annotations-13.0.jar`, `asm-5.0.3.jar` (+27).
- **Controller/service/repository (mẫu):** `AdminNftControllerService`, `ApiAdminController`, `ApiBlockController`, `ApiChainController`, `AdminAddressService`, `AdminAddressTransactionService`, `AdminAdminValidator`, `AdminAdminWalletService`, `AdminBAddressRepository`.
- **Class cấu hình/quyền (mẫu):** `BlockchainSettingsConfig`.
- **Điểm mở rộng tiềm năng theo tên class:** `AddressProcessor`, `AddressTransfersProcessor`, `AdminNftDataFetcherManager`, `AdminWeb3jManagerProvider`, `BlockProcessor`, `BlockchainThreadFactory`, `NftDataFetcherManager`, `NftProcessor`, `PipelineManager` (+3).

### web-plugin

- **JAR kiểm tra:** `ezyblockchain-sdk-0.0.3.jar`, `ezyblockchain-web-plugin-0.0.3.jar`; 153 class cấp cao nhất sau khi bỏ trùng theo tên package/class trong lane. SDK có thể lặp giữa các lane.
- **Package nổi bật:** `org.youngmonkeys.ezyblockchain.pagination`, `org.youngmonkeys.ezyblockchain.entity`, `org.youngmonkeys.ezyblockchain.model` (+22).
- **JAR thư viện khác:** `Java-WebSocket-1.3.8.jar`, `abi-5.0.0.jar`, `annotations-13.0.jar`, `asm-5.0.3.jar` (+27).
- **Controller/service/repository (mẫu):** `ApiAccountController`, `ApiBlockController`, `ApiChainController`, `ApiContractController`, `BChainRepository`, `BChainService`, `BNftRepository`, `BNftService`, `BTransactionRepository`.
- **Điểm mở rộng tiềm năng theo tên class:** `BlockchainThreadFactory`, `NftDataFetcherManager`, `Web3jManager`, `Web3jManagerProvider`, `WebNftDataFetcherManager`, `WebWeb3jManagerProvider`.

Class và resource xác nhận có cấu trúc mở rộng trong bản đóng gói, không cam kết API ổn định hoặc handler đã chạy qua mọi nhánh.

## Quan sát trên sandbox

Admin `/ezyblockchain/control-panel` và Web `/ezyblockchain/api/v1/chains/current` → 200; log Admin cảnh báo migration xóa index không tồn tại. Chưa nối ví hoặc chạy giao dịch.

## Lưu ý khi tích hợp

Tách schema/migration cho tích hợp ngoài. Cảnh báo khi migration xóa index không tồn tại cần điều tra, kể cả khi API danh sách trả 200.

[Về chỉ mục plugin](README.md)
