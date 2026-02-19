# Feature: 移除硬編碼 Admin 憑證

**狀態:** 已完成
**完成日期:** 2026-02-19
**相關計畫:** `docs/plans/2026-02-19-remove-hardcoded-admin-credentials.md`

---

## 目的

將 `init_db.py` 中硬編碼的 `admin` / `admin123` 憑證替換為必填的環境變數。若環境變數未設定，應用程式在啟動時會立即失敗（fail-fast）。

---

## 變更檔案

| 檔案 | 變更類型 | 說明 |
|------|----------|------|
| `backend/app/core/config.py` | 修改 | 新增 `ADMIN_USERNAME: str` 和 `ADMIN_PASSWORD: str` 必填欄位（無預設值） |
| `backend/app/db/init_db.py` | 重寫 | 改從 `settings` 讀取憑證，移除所有硬編碼字串 |
| `backend/tests/test_admin_credentials_config.py` | 新增 | 驗證 Settings 欄位型別、必填行為、CI 可靠性 |
| `backend/tests/test_init_db.py` | 新增 | 驗證 init_db 使用環境變數憑證、不重複建立使用者、密碼 hash 正確性 |
| `backend/.env.example` | 修改 | 新增 `ADMIN_USERNAME` / `ADMIN_PASSWORD` 說明與 placeholder |
| `backend/README.md` | 修改 | 移除舊的預設憑證說明，改為必填憑證指引 |

---

## 實作方式

### `config.py` — 必填欄位

```python
# Admin user credentials (required - no defaults, must be set via environment)
ADMIN_USERNAME: str
ADMIN_PASSWORD: str
```

`pydantic_settings.BaseSettings` 的欄位若無預設值，在 `Settings()` 實例化時若環境變數缺失會拋出 `ValidationError`，應用程式無法啟動。

### `init_db.py` — 讀取 settings

```python
from app.core.config import settings

def init_db(db: Session) -> None:
    user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if not user:
        user = User(
            username=settings.ADMIN_USERNAME,
            email="admin@example.com",
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
        )
        ...
```

### `.env` 本地開發值（不進 git）

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### `.env.example` 範本

```
# Admin User (required - no defaults, app will refuse to start if not set)
# Generate a strong password: python -c "import secrets; print(secrets.token_urlsafe(16))"
ADMIN_USERNAME="your-admin-username"
ADMIN_PASSWORD="change-this-before-deploying"
```

---

## 測試涵蓋

| 測試 | 驗證內容 |
|------|----------|
| `test_admin_username_read_from_env` | Settings 正確讀取 ADMIN_USERNAME |
| `test_admin_password_read_from_env` | Settings 正確讀取 ADMIN_PASSWORD |
| `test_admin_username_is_str` | 型別為 str |
| `test_admin_password_is_str` | 型別為 str |
| `test_missing_admin_username_raises` | 缺少欄位拋出 `ValidationError` |
| `test_missing_admin_password_raises` | 缺少欄位拋出 `ValidationError` |
| `test_init_db_uses_env_username` | init_db 使用 ADMIN_USERNAME，且密碼 hash 正確 |
| `test_init_db_does_not_create_hardcoded_admin` | 不建立硬編碼 `admin` 使用者 |
| `test_init_db_does_not_duplicate_user` | 重複呼叫不建立重複使用者 |

---

## Commits

| SHA | 說明 |
|-----|------|
| `1ac78e0` | feat: add required ADMIN_USERNAME and ADMIN_PASSWORD to settings |
| `aea2aa2` | test: fix test isolation - use patch.object instead of importlib.reload |
| `4165765` | test: use direct Settings() instantiation for CI-safe credential config tests |
| `37dc1d2` | test: use specific ValidationError instead of broad Exception in config tests |
| `8d9d8e3` | feat: init_db reads admin credentials from settings, removes hardcoded values |
| `2f221e1` | test: verify password hash correctness in test_init_db |
| `3194f8d` | docs: add ADMIN_USERNAME and ADMIN_PASSWORD to .env.example |
| `196e9ac` | docs: use placeholder username in .env.example to discourage copy-paste |
| `ce5e68d` | docs: update README to reflect required admin credentials, remove hardcoded defaults |
