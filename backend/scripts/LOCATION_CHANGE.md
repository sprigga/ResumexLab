# 腳本位置變更說明

**日期**: 2026-01-04
**版本**: 1.1

## 📁 位置變更

### 舊位置
```
project_root/
└── script/
    ├── alembic_helper.py
    ├── alembic_create_migration.sh
    ├── alembic_diagnose.sh
    ├── README_ALEMBIC_SCRIPTS.md
    └── QUICK_REFERENCE.md
```

### 新位置
```
project_root/
└── backend/
    └── scripts/
        ├── alembic_helper.py
        ├── alembic_create_migration.sh
        ├── alembic_diagnose.sh
        ├── README_ALEMBIC_SCRIPTS.md
        ├── QUICK_REFERENCE.md
        └── LOCATION_CHANGE.md (本文件)
```

## 🔧 使用方式更新

### 本機開發環境

**舊方式**：
```bash
# 從專案根目錄
python script/alembic_helper.py status
./script/alembic_create_migration.sh "描述"
./script/alembic_diagnose.sh
```

**新方式**：
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

## ✅ Docker 配置確認

### Dockerfile
```dockerfile
# backend/Dockerfile (第 40 行)
COPY . .
```
✓ 這會複製整個 backend 目錄，包含 scripts/

### docker-compose.yml
```yaml
# docker-compose.yml
services:
  backend:
    volumes:
      - ./backend/data:/app/data  # 只掛載 data 目錄
```
✓ scripts/ 目錄會被複製到容器內，不需要額外掛載

## 📝 路徑邏輯更新

### Python 腳本 (alembic_helper.py)

**修改內容**：
```python
# 原本 (位於 project_root/script/)
self.script_dir = Path(__file__).parent.absolute()  # script/
self.project_root = self.script_dir.parent          # project_root/
self.backend_dir = self.project_root / "backend"    # project_root/backend/

# 更新後 (位於 backend/scripts/)
self.script_dir = Path(__file__).parent.absolute()  # backend/scripts/
self.backend_dir = self.script_dir.parent           # backend/
self.project_root = self.backend_dir.parent         # project_root/
```

### Bash 腳本 (alembic_create_migration.sh, alembic_diagnose.sh)

**修改內容**：
```bash
# 原本 (位於 project_root/script/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"

# 更新後 (位於 backend/scripts/)
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

## 🔄 遷移檢查清單

- [x] 移動所有 alembic 相關腳本到 backend/scripts/
- [x] 移動相關文件到 backend/scripts/
- [x] 更新 Python 腳本中的路徑引用
- [x] 更新 Bash 腳本中的路徑引用
- [x] 測試所有腳本功能正常
- [x] 確認 Dockerfile 會複製 scripts 目錄
- [x] 確認 docker-compose.yml 配置正確
- [x] 更新 .gitignore 排除備份檔案

## 📚 相關文件

- **詳細使用說明**: `README_ALEMBIC_SCRIPTS.md`
- **快速參考**: `QUICK_REFERENCE.md`
- **理論知識**: `../docs/Alembic.md`

## ⚠️ 重要提醒

1. **工作目錄**: 執行腳本前請確保在 `backend/` 目錄
2. **Docker 環境**: 容器內已在 `/app` 目錄，直接執行即可
3. **路徑引用**: 所有腳本內部路徑已更新，無需手動修改

---

**最後更新**: 2026-01-04
**作者**: Polo (林鴻全)
