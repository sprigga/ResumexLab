# Alembic 腳本快速參考

## 🚀 最常用的指令

### 日常操作

```bash
# 檢查狀態
python scripts/alembic_helper.py status

# 創建新遷移
./scripts/alembic_create_migration.sh "描述變更內容"

# 執行遷移
python scripts/alembic_helper.py migrate
```

### 問題處理

```bash
# 診斷問題
./scripts/alembic_diagnose.sh

# 修復 SQLite 兼容性
python scripts/alembic_helper.py fix-sqlite

# 回滾變更
python scripts/alembic_helper.py rollback
```

---

## 📋 完整指令速查

### alembic_helper.py

| 指令 | 功能 | 範例 |
|------|------|------|
| `status` | 檢查當前狀態 | `python scripts/alembic_helper.py status` |
| `check` | 健康檢查 | `python scripts/alembic_helper.py check` |
| `backup` | 備份資料庫 | `python scripts/alembic_helper.py backup` |
| `migrate` | 執行遷移 | `python scripts/alembic_helper.py migrate` |
| `stamp` | 標記版本 | `python scripts/alembic_helper.py stamp` |
| `fix-sqlite` | 修復 SQLite | `python scripts/alembic_helper.py fix-sqlite` |
| `rollback` | 回滾 | `python scripts/alembic_helper.py rollback` |
| `help` | 顯示幫助 | `python scripts/alembic_helper.py help` |

### alembic_create_migration.sh

```bash
# 創建遷移
./scripts/alembic_create_migration.sh "遷移描述"

# 創建並自動應用
./scripts/alembic_create_migration.sh "遷移描述" --apply
```

### alembic_diagnose.sh

```bash
# 執行診斷
./scripts/alembic_diagnose.sh
```

---

## 🔄 典型工作流程

### 新增功能

```bash
# 1. 修改 Model
vim backend/app/models/user.py

# 2. 創建遷移
./scripts/alembic_create_migration.sh "新增使用者頭像欄位"

# 3. 檢查生成的檔案（如有 SQLite 問題會自動提示修復）

# 4. 應用遷移
python scripts/alembic_helper.py migrate

# 5. 驗證
python scripts/alembic_helper.py status
```

### 遇到問題

```bash
# 1. 診斷
./scripts/alembic_diagnose.sh

# 2. 修復（根據診斷建議）
python scripts/alembic_helper.py fix-sqlite

# 3. 重試
python scripts/alembic_helper.py migrate
```

---

## ⚡ 常見問題快速解決

| 問題 | 解決方案 |
|------|----------|
| 資料庫已有表但未標記版本 | `python scripts/alembic_helper.py stamp` |
| ALTER COLUMN 錯誤 | `python scripts/alembic_helper.py fix-sqlite` |
| 需要回滾變更 | `python scripts/alembic_helper.py rollback` |
| 不確定系統狀態 | `./scripts/alembic_diagnose.sh` |
| 需要備份 | `python scripts/alembic_helper.py backup` |

---

## 📁 檔案位置

- 腳本目錄: `scripts/`
- 遷移檔案: `alembic/versions/`
- 資料庫: `data/resume.db`
- 備份: `data/resume_backup_*.db`
- 配置: `alembic.ini`

---

**更多資訊**: 參見 `scripts/README_ALEMBIC_SCRIPTS.md` 或 `docs/Alembic.md`
