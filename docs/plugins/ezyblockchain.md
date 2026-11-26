# ezyblockchain

Chains, tokens, and wallet address management.

- **Marketplace version on core 1.5.9:** `0.0.3`.
- **Verified modules:** `admin-plugin`, `web-plugin`.
- **Installation:** Get through Admin. See the environment and general limits in [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/ezyblockchain` | `org.youngmonkeys.ezyblockchain` | Not declared |
| `web-plugin` — `web/plugins/ezyblockchain` | `org.youngmonkeys.ezyblockchain` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 16 method/URI combinations identified; representative sample:

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

**web-plugin** — 11 method/URI combinations identified; representative sample:

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

- **admin-plugin – Menus (final keys and paths in menus.properties):** `ezyblockchain: /`, `control_panel: /control-panel`, `chain_list: /chains`, `add_chain: ~/chains/add`, `edit_chain: ~/chains/{chainId}/edit`, `chain_details: ~/chains/{chainId}`.

- **admin-plugin – Template:** `ezyblockchain/chains/add.html`, `ezyblockchain/chains/details.html`, `ezyblockchain/chains/edit.html`, `ezyblockchain/chains/list.html`, `ezyblockchain/chains/scripts.html`, `ezyblockchain/control-panel/index.html`.

## Data and migrations

- **Table in the DDL packaging (9):** `ezyblockchain_address_transactions`, `ezyblockchain_addresses`, `ezyblockchain_blocks`, `ezyblockchain_chains`, `ezyblockchain_nfts`, `ezyblockchain_processed_block_height`, `ezyblockchain_processing_block_height`, `ezyblockchain_transactions`, `ezyblockchain_transfers`.
- **Class with JPA Entity/MappedSuperclass):** `BAddress`, `BAddressTransaction`, `BBlock`, `BChain`, `BNft`, `BProcessedBlockHeight`, `BProcessingBlockHeight`, `BTransaction`, `BTransfer`.
- **SQL admin-plugin (2 files):** `resources/scripts/scripts.sql`, `resources/scripts/alter_tables_1.sql`.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `ezyblockchain-admin-plugin-0.0.3.jar`, `ezyblockchain-sdk-0.0.3.jar`; 178 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyblockchain.pagination`, `org.youngmonkeys.ezyblockchain.entity`, `org.youngmonkeys.ezyblockchain.model` (+32).
- **Other library JARs:** `Java-WebSocket-1.3.8.jar`, `abi-5.0.0.jar`, `annotations-13.0.jar`, `asm-5.0.3.jar` (+27).
- **Controllers, services, and repositories (sample):** `AdminNftControllerService`, `ApiAdminController`, `ApiBlockController`, `ApiChainController`, `AdminAddressService`, `AdminAddressTransactionService`, `AdminAdminValidator`, `AdminAdminWalletService`, `AdminBAddressRepository`.
- **Configuration and permission classes (sample):** `BlockchainSettingsConfig`.
- **Potential extension points based on class names:** `AddressProcessor`, `AddressTransfersProcessor`, `AdminNftDataFetcherManager`, `AdminWeb3jManagerProvider`, `BlockProcessor`, `BlockchainThreadFactory`, `NftDataFetcherManager`, `NftProcessor`, `PipelineManager` (+3).

### web-plugin

- **JARs inspected:** `ezyblockchain-sdk-0.0.3.jar`, `ezyblockchain-web-plugin-0.0.3.jar`; 153 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.ezyblockchain.pagination`, `org.youngmonkeys.ezyblockchain.entity`, `org.youngmonkeys.ezyblockchain.model` (+22).
- **Other library JARs:** `Java-WebSocket-1.3.8.jar`, `abi-5.0.0.jar`, `annotations-13.0.jar`, `asm-5.0.3.jar` (+27).
- **Controllers, services, and repositories (sample):** `ApiAccountController`, `ApiBlockController`, `ApiChainController`, `ApiContractController`, `BChainRepository`, `BChainService`, `BNftRepository`, `BNftService`, `BTransactionRepository`.
- **Potential extension points based on class names:** `BlockchainThreadFactory`, `NftDataFetcherManager`, `Web3jManager`, `Web3jManagerProvider`, `WebNftDataFetcherManager`, `WebWeb3jManagerProvider`.

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/ezyblockchain/control-panel` and Web `/ezyblockchain/api/v1/chains/current` returned 200. Admin logs warned that a migration tried to drop a nonexistent index. No wallet connection or transaction was tested.

## Integration notes

Keep schemas and migrations separate for external integrations. Investigate warnings about migrations dropping nonexistent indexes even when the list API returns 200.

[Back to the plugin index](README.md)
