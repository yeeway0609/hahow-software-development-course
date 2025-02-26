# 「踏出程式新手村！掌握敏捷式軟體開發流程」專案範例

這是「踏出程式新手村！掌握敏捷式軟體開發流程」課程的後端點餐系統範例，此專案的重點在於實際體驗軟體開發流程。

## Getting Started

### Prerequisites

- 需要安裝 Python 3.11，或是用 [pyenv](https://github.com/pyenv/pyenv) 版本控制套件
- 設定好 MongoDB（可以自行在電腦建立，或是參考課堂教學設定 MongoDB Atlas）
- 申請一個 Heroku 帳號

### Installation

1. 執行 `make init` 來安裝必要套件
2. 執行 `make setupMongo` 來將範例資料匯入創建好的 MongoDB（注意：這個執行一次就好）
3. 執行 `make all` 來啟動伺服器，若能啟動伺服器則設定成功

### Useful Commands

- `make format`： 自動排版專案中所有的 code
- `make format-check`： 確認 code 是否有排版問題，但不主動重新排版
- `make lint`： 檢查 code 是否符合 PEP8 coding style
- `make test-unit`： 執行專案中所有的 unit tests
- `make test-inte`： 執行專案中所有的 integration tests
- `make test-all`： 執行專案中所有的 tests
- `make run`： 在電腦上啟動點餐系統後端伺服器

## 作業練習

### 1. Design Doc

[點餐系統後端 API 設計文件](./design_doc/README.md)

### 2. API Implementation

- [Get Order](./order_system/handler/get_order.py)
- [Create Order](./order_system/handler/create_order.py)

### 3. Unit Test

- [GetOrder](./tst/unit/handler/test_get_order.py)
- [CreateOrder](./tst/unit/handler/test_create_order.py)

### 4. Integration Test
- [Get Order API 與 API Handler](./tst/integration/test_api_handler_inte.py)
- [Create Order API 與 API Handler](./tst/integration/test_api_handler_inte.py)
- [Get Order API 與 Order DAO](./tst/integration/test_handler_dao_inte.py)
- [Create Order API 與 Order DAO](./tst/integration/test_handler_dao_inte.py)