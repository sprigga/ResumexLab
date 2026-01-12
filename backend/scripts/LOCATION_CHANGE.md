# 腳本位置說明

**日期**: 2026-01-05
**版本**: 1.2

## 📁 當前位置

### 目錄結構
```
backend/
└── scripts/
    ├── alembic_helper.py
    ├── alembic_create_migration.sh
    ├── alembic_diagnose.sh
    ├── README_ALEMBIC_SCRIPTS.md
    ├── QUICK_REFERENCE.md
    └── LOCATION_CHANGE.md (本文件)
```

### 重要說明
**所有腳本都位於 `backend/scripts/` 目錄（複數形式）**，執行時請確保：
1. 在 `backend/` 目錄下執行命令
2. 使用 `scripts/` 路徑（不是 `script/`）

## 🔧 使用方式

### 本機開發環境

```bash
# 切換到 backend 目錄
cd backend

# 執行腳本
python scripts/alembic_helper.py status
./scripts/alembic_create_migration.sh "描述"
./scripts/alembic_diagnose.sh
```

### Docker 容器環境

**容器內路徑**：
```
/app/
├── scripts/          # 腳本目錄
│   ├── alembic_helper.py
│   ├── alembic_create_migration.sh
│   ├── alembic_diagnose.sh
│   ├── README_ALEMBIC_SCRIPTS.md
│   └── QUICK_REFERENCE.md
├── alembic/         # Alembic 配置
├── app/             # 應用程式碼
└── data/            # 資料庫檔案
```

**使用方式**：
```bash
# 進入容器
docker exec -it resumexlab-backend bash

# 在容器內執行（已在 /app 目錄）
python scripts/alembic_helper.py status
./scripts/alembic_create_migration.sh "描述"
./scripts/alembic_diagnose.sh
```

## 📝 路徑邏輯

### Python 腳本 (alembic_helper.py)

**當前實作**：
```python
# 位於 backend/scripts/
self.script_dir = Path(__file__).parent.absolute()  # backend/scripts/
self.backend_dir = self.script_dir.parent           # backend/
self.project_root = self.backend_dir.parent         # project_root/
```

### Bash 腳本 (alembic_create_migration.sh, alembic_diagnose.sh)

**當前實作**：
```bash
# 位於 backend/scripts/
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # backend/scripts/
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"                          # backend/
PROJECT_ROOT="$(dirname "$BACKEND_DIR")"                        # project_root/
```

## 🧪 測試結果

所有腳本已測試並確認正常運作：

### Python 腳本測試
```bash
$ cd backend
$ python scripts/alembic_helper.py status
✓ 資料庫存在: /path/to/backend/data/resume.db
✓ 找到 2 個遷移檔案
...

$ python scripts/alembic_helper.py check
✓ 所有檢查通過！
```

### Bash 腳本測試
```bash
$ cd backend
$ ./scripts/alembic_diagnose.sh
✓ 虛擬環境存在
✓ Alembic 已安裝
...
```

## 🔄 設定檢查清單

- [x] 所有 alembic 相關腳本位於 backend/scripts/
- [x] 相關文件已更新至使用正確路徑 (scripts/)
- [x] Python 腳本中的路徑引用正確
- [x] Bash 腳本中的路徑引用正確
- [x] 文件中的範例使用正確路徑 (scripts/)
- [x] Dockerfile 會複製 scripts 目錄
- [x] docker-compose.yml 配置正確
- [x] .gitignore 排除備份檔案

## 📚 相關文件

- **詳細使用說明**: `README_ALEMBIC_SCRIPTS.md`
- **快速參考**: `QUICK_REFERENCE.md`
- **理論知識**: `../docs/Alembic.md`

## ⚠️ 重要提醒

1. **工作目錄**: 執行腳本前請確保在 `backend/` 目錄
2. **Docker 環境**: 容器內已在 `/app` 目錄，直接執行即可
3. **路徑名稱**: 使用 `scripts/` (複數) 不是 `script/` (單數)

---

**最後更新**: 2026-01-05
**作者**: Polo (林鴻全)
