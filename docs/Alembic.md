# Alembic 資料庫遷移指南

**專案**: ResumeXLab - 個人履歷管理系統
**更新日期**: 2025-12-30
**作者**: Polo (林鴻全)

---

## 📋 目錄

1. [簡介](#簡介)
2. [進入 Backend Container](#進入-backend-container)
3. [常用 Alembic 指令](#常用-alembic-指令)
4. [常見問題與解決方案](#常見問題與解決方案)
5. [工作流程](#工作流程)
6. [重要檔案位置](#重要檔案位置)

---

## 簡介

Alembic 是 SQLAlchemy 的資料庫遷移工具，用於管理資料庫結構的變更。本專案使用 Alembic 來管理 SQLite 資料庫的版本控制。

### 為什麼需要 Alembic？

- ✅ **版本控制**: 追蹤資料庫結構的所有變更歷史
- ✅ **團隊協作**: 確保所有開發者的資料庫結構一致
- ✅ **回滾能力**: 可以輕鬆回退到之前的資料庫版本
- ✅ **自動生成**: 根據 SQLAlchemy Model 自動生成遷移腳本

---

## 進入 Backend Container

### 方法 1：進入 Container 後執行指令

```bash
# 進入 backend container
docker exec -it resumexlab-backend bash

# 現在您位於 /app 目錄，可以執行任何 Alembic 指令
alembic current

# 操作完成後離開
exit
```

### 方法 2：直接從主機執行指令（不進入 Container）

```bash
# 查看目前版本
docker exec resumexlab-backend alembic current

# 升級資料庫
docker exec resumexlab-backend alembic upgrade head

# 建立新遷移
docker exec resumexlab-backend alembic revision --autogenerate -m "描述變更"
```

---

## 常用 Alembic 指令

### 📊 查看版本狀態

```bash
# 查看目前資料庫版本
alembic current
# 輸出示例: d711f173f9e3 (head)

# 查看所有遷移版本歷史
alembic history

# 查看最新的遷移版本
alembic heads
```

### ⬆️ 升級資料庫

```bash
# 升級到最新版本
alembic upgrade head

# 升級到特定版本
alembic upgrade <revision_id>

# 升級一個版本
alembic upgrade +1
```

### ⬇️ 降級資料庫

```bash
# 降級到上一個版本
alembic downgrade -1

# 降級到特定版本
alembic downgrade <revision_id>

# 降級到基礎版本（空資料庫）
alembic downgrade base
```

### ✏️ 建立遷移

```bash
# 自動生成遷移（根據 Model 變更）
alembic revision --autogenerate -m "描述您的變更"

# 手動建立空白遷移腳本
alembic revision -m "手動遷移"
```

### 🔍 其他實用指令

```bash
# 顯示遷移 SQL（不實際執行）
alembic upgrade head --sql

# 驗證遷移腳本是否有錯誤
alembic check

# 查看說明
alembic --help
```

---

## 常見問題與解決方案

### ❌ 問題 1：`table already exists` 錯誤

**錯誤訊息**：
```bash
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) table certifications already exists
```

**原因分析**：
- 資料庫表已經存在（可能是直接使用 SQLAlchemy 或其他方式建立）
- 但 Alembic 的 `alembic_version` 表沒有記錄這個遷移版本
- Alembic 認為需要建立表，但表已經存在，導致衝突

**檢查狀態**：
```bash
# 查看 Alembic 版本（可能沒有輸出或顯示 <base>）
alembic current

# 查看資料庫中實際存在的表
sqlite3 /app/data/resume.db ".tables"
```

**解決方案 A：標記資料庫為最新版本（推薦）**

告訴 Alembic 資料庫已經在這個版本了：

```bash
# 標記為最新版本
alembic stamp head

# 驗證是否成功
alembic current
# 應該輸出: d711f173f9e3 (head)
```

**解決方案 B：手動插入版本記錄**

```bash
# 插入版本記錄到 alembic_version 表
sqlite3 /app/data/resume.db "INSERT INTO alembic_version (version_num) VALUES ('d711f173f9e3');"
```

**解決方案 C：重建資料庫（如果資料不重要）**

```bash
# 1. 進入 container
docker exec -it resumexlab-backend bash

# 2. 刪除舊資料庫
rm /app/data/resume.db

# 3. 執行遷移（會建立新資料庫）
alembic upgrade head
```

---

### ❌ 問題 2：`Target database is not up to date` 錯誤

**錯誤訊息**：
```bash
ERROR [alembic.util.messaging] Target database is not up to date.
  FAILED: Target database is not up to date.
```

**原因**：
- 嘗試建立新遷移時，資料庫不是最新版本
- Alembic 要求資料庫必須在最新版本才能建立新遷移

**解決方案**：
```bash
# 1. 先升級到最新版本
alembic upgrade head

# 2. 再建立新遷移
alembic revision --autogenerate -m "描述變更"
```

---

### ❌ 問題 3：遷移腳本生成錯誤

**症狀**：
- `--autogenerate` 沒有偵測到 Model 變更
- 生成的遷移腳本內容不正確

**解決方案**：

```bash
# 1. 確認 Model 檔案是否正確導入
# 檢查 backend/app/models.py 和 backend/app/database.py

# 2. 確認 alembic/env.py 中的 target_metadata 是否正確設定
# 應該包含所有的 Model

# 3. 清除 Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# 4. 重新生成遷移
alembic revision --autogenerate -m "描述變更"
```

---

### ❌ 問題 4：如何回滾遷移

**場景**：
- 剛建立的遷移有問題
- 需要回到之前的版本

**解決方案**：
```bash
# 1. 查看歷史版本，找到要回退的版本
alembic history

# 2. 降級到上一個版本
alembic downgrade -1

# 3. 如果需要回退到特定版本
alembic downgrade <revision_id>

# 4. 刪除錯誤的遷移檔案（如果需要）
# 刪除 alembic/versions/ 目錄中對應的 .py 檔案
```

---

## 工作流程

### 🔄 標準開發流程

當您需要修改資料庫結構時，請遵循以下步驟：

#### 1. 修改 SQLAlchemy Model

編輯 `backend/app/models.py`，新增或修改 Model 類別：

```python
# 例如：新增一個欄位
class WorkExperience(Base):
    __tablename__ = "work_experience"

    # 原有欄位...

    # 新增欄位
    salary = Column(Integer, nullable=True)  # 薪資
```

#### 2. 建立遷移腳本

```bash
# 進入 container 或直接執行
docker exec -it resumexlab-backend bash

# 生成遷移
alembic revision --autogenerate -m "新增工作經歷薪資欄位"
```

#### 3. 檢查生成的遷移腳本

```bash
# 查看生成的檔案
cat alembic/versions/xxxxxxxxxxxx_新增工作經歷薪資欄位.py
```

檢查 `upgrade()` 和 `downgrade()` 函數是否正確：

```python
def upgrade():
    # 檢查這裡的運作是否符合預期
    op.add_column('work_experience', sa.Column('salary', sa.Integer(), nullable=True))

def downgrade():
    # 檢查回滾運作是否正確
    op.drop_column('work_experience', 'salary')
```

#### 4. 執行遷移

```bash
# 升級資料庫
alembic upgrade head

# 驗證版本
alembic current
```

#### 5. 測試應用程式

```bash
# 重啟 backend 服務（如果需要）
docker restart resumexlab-backend

# 測試 API 是否正常運作
curl http://localhost:58433/health
```

---

### 🚀 生產環境部署流程

```bash
# 1. 備份現有資料庫
cp /app/data/resume.db /app/data/resume_backup_$(date +%Y%m%d_%H%M%S).db

# 2. 確認目前版本
alembic current

# 3. 查看待套用的遷移
alembic history

# 4. 執行升級
alembic upgrade head

# 5. 驗證升級結果
alembic current

# 6. 測試應用程式功能
```

---

## 重要檔案位置

### Container 內路徑

| 檔案/目錄 | 路徑 | 說明 |
|----------|------|------|
| Alembic 設定檔 | `/app/alembic.ini` | Alembic 主設定檔 |
| 遷移腳本目錄 | `/app/alembic/versions/` | 存放所有遷移腳本 |
| 環境設定 | `/app/alembic/env.py` | Alembic 執行環境設定 |
| 資料庫檔案 | `/app/data/resume.db` | SQLite 資料庫檔案 |
| Model 定義 | `/app/app/models.py` | SQLAlchemy Model 定義 |
| 資料庫設定 | `/app/app/database.py` | 資料庫連線設定 |

### 主機路徑（對應的 Docker Volume）

| Container 路徑 | 主機路徑 | 說明 |
|---------------|----------|------|
| `/app/data` | `./backend/data` | 資料庫檔案存放目錄 |

---

## 實戰範例

### 範例 1：新增欄位

```python
# 1. 修改 Model
# backend/app/models.py
class User(Base):
    # ... 原有欄位
    avatar_url = Column(String(500), nullable=True)  # 新增頭像 URL
```

```bash
# 2. 建立遷移
docker exec resumexlab-backend alembic revision --autogenerate -m "新增使用者頭像欄位"

# 3. 執行遷移
docker exec resumexlab-backend alembic upgrade head
```

### 範例 2：新增表

```python
# 1. 新增 Model
# backend/app/models.py
class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name_zh = Column(String(100))
    name_en = Column(String(100))
    proficiency = Column(String(50))
```

```bash
# 2. 建立遷移
docker exec resumexlab-backend alembic revision --autogenerate -m "新增技能表"

# 3. 執行遷移
docker exec resumexlab-backend alembic upgrade head
```

### 範例 3：處理版本衝突（本次實際案例）

```bash
# 問題：資料庫表已存在，但 Alembic 沒有版本記錄
# 錯誤：sqlite3.OperationalError: table certifications already exists

# 解決：標記為最新版本
docker exec resumexlab-backend alembic stamp head

# 驗證
docker exec resumexlab-backend alembic current
# 輸出: d711f173f9e3 (head)
```

---

## 最佳實踐

### ✅ DO（應該做的）

1. **每次修改 Model 後立即建立遷移**
   ```bash
   alembic revision --autogenerate -m "清晰的描述"
   ```

2. **檢查生成的遷移腳本**
   - 確認 `upgrade()` 和 `downgrade()` 邏輯正確
   - 避免遺失資料的操作

3. **使用有意義的遷移描述**
   ```bash
   # 好的範例
   alembic revision --autogenerate -m "新增使用者頭像欄位"

   # 不好的範例
   alembic revision --autogenerate -m "update"
   ```

4. **升級前備份資料庫**
   ```bash
   cp /app/data/resume.db /app/data/resume_backup_$(date +%Y%m%d_%H%M%S).db
   ```

5. **保持遷移順序性**
   - 不要跳過版本
   - 依序執行每個遷移

### ❌ DON'T（不該做的）

1. **不要直接修改資料庫結構**
   - 總是使用 Alembic 遷移
   - 避免手動執行 SQL DDL

2. **不要跳過中間的遷移版本**
   ```bash
   # 不好的做法
   alembic upgrade version_5  # 如果目前在 version_3

   # 正確的做法
   alembic upgrade head  # 依序升級
   ```

3. **不要刪除已執行的遷移檔案**
   - 這會導致版本歷史中斷
   - 如果真的需要，使用 `alembic downgrade` 先回退

4. **不要在生產環境使用 `--autogenerate`**
   - 先在開發環境測試
   - 檢查生成的腳本
   - 確認無誤後再部署

5. **不要忽視 `downgrade()` 函數**
   - 確保回滾邏輯正確
   - 測試回滾是否可行

---

## 除錯技巧

### 查看詳細執行資訊

```bash
# 開啟詳細輸出模式
alembic upgrade head --verbose
```

### 查看將要執行的 SQL

```bash
# 顯示 SQL 但不執行
alembic upgrade head --sql
```

### 檢查資料庫實際結構

```bash
# 進入 SQLite
sqlite3 /app/data/resume.db

# 查看 schema
.schema

# 查看表
.tables

# 查看特定表結構
.schema table_name
```

### 清除快取並重試

```bash
# 清除 Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# 重新執行遷移
alembic upgrade head
```

---

## 參考資源

- [Alembic 官方文件](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 官方文件](https://www.sqlalchemy.org/)
- [FastAPI 資料庫教學](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

## 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0 | 2025-12-30 | 初版建立，記錄常見問題與解決方案 |

---

## 附錄：完整 Alembic 指令速查表

```bash
# === 版本查詢 ===
alembic current          # 查看目前版本
alembic history          # 查看完整歷史
alembic heads            # 查看最新版本
alembic branches          # 查看分支

# === 升級操作 ===
alembic upgrade head     # 升級到最新
alembic upgrade +1       # 升級一個版本
alembic upgrade <rev>    # 升級到指定版本

# === 降級操作 ===
alembic downgrade -1     # 降級一個版本
alembic downgrade base   # 降級到初始狀態
alembic downgrade <rev>  # 降級到指定版本

# === 建立遷移 ===
alembic revision -m "描述"                    # 手動建立空白遷移
alembic revision --autogenerate -m "描述"    # 自動生成遷移

# === 特殊操作 ===
alembic stamp head      # 標記資料庫為最新版本（不執行遷移）
alembic upgrade head --sql    # 顯示 SQL（不執行）
alembic check           # 驗證遷移腳本

# === 除錯 ===
alembic --help          # 查看說明
alembic upgrade head --verbose  # 詳細輸出模式
```

---

**最後更新**: 2025-12-30
**維護者**: Polo (林鴻全)
**專案**: ResumeXLab
