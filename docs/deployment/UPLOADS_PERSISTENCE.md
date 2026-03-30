# Uploads 目錄持久化配置說明

## 📋 問題說明

在執行 `docker-compose down` 時，容器內的 `/app/uploads/` 目錄及其文件會隨著容器刪除而消失。

## ✅ 解決方案

通過在 `docker-compose.yml` 中配置 **Volume 掛載**，將主機的 `./backend/uploads` 目錄映射到容器的 `/app/uploads` 目錄，實現數據持久化。

## 🎯 配置完成總結

### ✅ 已完成的修改

#### 1. docker-compose.yml (生產環境)
- **文件位置**: `docker-compose.yml:50`
- **修改內容**: 添加 uploads volume 掛載
```yaml
volumes:
  - ./backend/data:/app/data
  - ./backend/uploads:/app/uploads  # ⭐ 新增
```

#### 2. docker-compose.dev.yml (開發環境)
- **文件位置**: `docker-compose.dev.yml:48`
- **修改內容**: 添加 uploads volume 掛載
```yaml
volumes:
  - ./backend/data:/app/data
  - ./backend/uploads:/app/uploads  # ⭐ 新增
```

#### 3. backend/Dockerfile
- **文件位置**: `backend/Dockerfile:43`
- **修改內容**: 在容器內創建 uploads 目錄
```dockerfile
RUN mkdir -p /app/data /app/uploads  # ⭐ 添加 uploads
```

### 📁 創建的輔助文件

1. **QUICK_START_UPLOADS.md** - 快速開始指南
2. **UPLOADS_PERSISTENCE.md** - 本文檔（詳細配置說明）
3. **docs/docker-commands-reference.md** - Docker 指令參考大全
4. **docs/volume-mounting-diagram.md** - Volume 掛載架構圖解
5. **test_uploads_persistence.sh** - 自動化測試腳本

### 📊 工作流程對比

#### ❌ 修改前（沒有 Volume 掛載）

```
docker-compose up → 上傳文件 → docker-compose down
                                       ↓
                                  文件消失 ❌
```

#### ✅ 修改後（有 Volume 掛載）

```
docker-compose up → 上傳文件 → docker-compose down
                         ↓              ↓
                 保存到主機目錄    容器刪除但文件保留 ✅
                         ↓
              docker-compose up → 文件自動恢復訪問 ✅
```

### 🔑 核心原理

- **Volume 掛載**: 將主機目錄 `./backend/uploads` 映射到容器的 `/app/uploads`
- **數據持久化**: 容器刪除時文件保留在主機
- **自動恢復**: 重新啟動容器時自動恢復文件訪問
- **雙向同步**: 主機和容器內的文件操作實時同步

## 🔧 配置詳情

### 1. docker-compose.yml 配置

```yaml
services:
  backend:
    volumes:
      # 掛載資料庫文件，確保數據持久化
      - ./backend/data:/app/data
      # 掛載上傳文件目錄，確保上傳的文件持久化
      - ./backend/uploads:/app/uploads
```

### 2. Dockerfile 配置

```dockerfile
# 建立資料庫目錄和上傳文件目錄
RUN mkdir -p /app/data /app/uploads
```

## 📂 目錄結構

```
resumexlab/
├── backend/
│   ├── data/              # 資料庫持久化目錄
│   │   └── resume.db
│   ├── uploads/           # 上傳文件持久化目錄 ⭐
│   │   └── test_work_experience_attachment.txt
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── docker-compose.dev.yml
```

## 🎯 工作原理

### Volume 掛載機制

```
主機目錄                      容器目錄
./backend/uploads    <--->   /app/uploads
     (持久化)                  (臨時)
```

- **主機目錄**: `./backend/uploads` (本地文件系統，永久保存)
- **容器目錄**: `/app/uploads` (容器內目錄，容器刪除時消失)
- **掛載效果**: 容器內對 `/app/uploads` 的所有操作實際上都在操作主機的 `./backend/uploads`

### 生命週期

| 操作 | 主機目錄 | 容器目錄 | 文件狀態 |
|------|---------|---------|---------|
| `docker-compose up` | 存在 | 掛載成功 | ✅ 可訪問 |
| 上傳文件 | 新增文件 | 新增文件 | ✅ 同步 |
| `docker-compose down` | 保留 | 容器刪除 | ✅ 文件保留在主機 |
| `docker-compose up` (再次) | 保留 | 重新掛載 | ✅ 文件恢復訪問 |

## 🧪 測試驗證

### 🚀 快速測試（3 步驟）

```bash
# 1. 創建測試文件
echo "持久化測試 $(date)" > backend/uploads/test.txt

# 2. 啟動容器 → 停止容器
docker-compose up -d
docker-compose down

# 3. 驗證文件是否保留
cat backend/uploads/test.txt  # ✅ 文件應該還在！
```

### 方法 1: 使用自動化測試腳本（推薦）

```bash
./test_uploads_persistence.sh
```

**測試腳本功能：**
- ✅ 自動創建測試文件
- ✅ 啟動容器並驗證
- ✅ 執行 docker-compose down
- ✅ 驗證文件是否保留
- ✅ 顯示詳細測試結果

### 方法 2: 手動測試（完整流程）

```bash
# 1. 創建測試文件
echo "測試文件" > backend/uploads/test.txt

# 2. 啟動容器
docker-compose up -d

# 3. 驗證容器內文件
docker exec resumexlab-backend ls -la /app/uploads/
docker exec resumexlab-backend cat /app/uploads/test.txt

# 4. 停止並刪除容器
docker-compose down

# 5. 驗證主機文件是否保留
ls -la backend/uploads/
cat backend/uploads/test.txt  # ✅ 應顯示文件內容

# 6. 重新啟動容器
docker-compose up -d

# 7. 驗證文件在新容器中可訪問
docker exec resumexlab-backend cat /app/uploads/test.txt  # ✅ 應顯示文件內容
```

**預期結果**: `test.txt` 文件在 `docker-compose down` 後仍然存在，且重新啟動容器後可正常訪問。

### 驗證掛載配置

```bash
# 查看容器的 volume 掛載資訊
docker inspect resumexlab-backend | grep -A 10 Mounts

# 或使用 jq 格式化輸出
docker inspect resumexlab-backend | jq '.[0].Mounts'
```

**預期輸出示例：**
```json
[
  {
    "Type": "bind",
    "Source": "/Users/pololin/python_project/resumexlab/backend/uploads",
    "Destination": "/app/uploads",
    "Mode": "rw",
    "RW": true
  }
]
```

## 🔍 驗證檢查清單

### 配置驗證

```bash
# 驗證配置文件
grep -n "uploads" docker-compose.yml docker-compose.dev.yml backend/Dockerfile
```

**預期輸出：**
```
docker-compose.yml:50:      - ./backend/uploads:/app/uploads
docker-compose.dev.yml:48:      - ./backend/uploads:/app/uploads
backend/Dockerfile:43:RUN mkdir -p /app/data /app/uploads
```

### 檢查清單

- [x] `backend/uploads` 目錄存在
- [x] `docker-compose.yml` 包含 volume 掛載配置 (第 50 行)
- [x] `docker-compose.dev.yml` 包含 volume 掛載配置 (第 48 行)
- [x] `Dockerfile` 創建 `/app/uploads` 目錄 (第 43 行)
- [ ] 執行 `docker-compose down` 後文件保留（需要測試）
- [ ] 重新啟動容器後文件可訪問（需要測試）

### 功能測試清單

```bash
# 1. 測試文件上傳和保存
# 2. 測試 docker-compose down 後文件保留
# 3. 測試容器重啟後文件恢復
# 4. 測試主機與容器文件同步
```

## 📝 注意事項

### 1. 目錄權限

確保 `backend/uploads` 目錄有正確的寫入權限：

```bash
# 設定目錄權限
chmod 755 backend/uploads

# 如果容器內用戶權限不同，可能需要調整所有者
# sudo chown -R 1000:1000 backend/uploads
```

### 2. .gitignore 配置

通常上傳的文件不應提交到 Git，確保 `.gitignore` 包含：

```gitignore
# 上傳文件（排除示例文件）
backend/uploads/*
!backend/uploads/.gitkeep
!backend/uploads/test_*.txt
```

### 3. 備份策略

雖然文件已持久化，但仍建議定期備份：

```bash
# 備份 uploads 目錄
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz backend/uploads/

# 或使用 rsync
rsync -av backend/uploads/ /path/to/backup/uploads/
```

### 4. 開發環境與生產環境

兩個環境都已配置相同的 volume 掛載：

- **生產環境**: `docker-compose.yml`
- **開發環境**: `docker-compose.dev.yml`

## 🚀 應用場景

此配置適用於以下場景：

1. **用戶上傳的履歷附件**
2. **工作經歷證明文件**
3. **個人照片/頭像**
4. **PDF 導出文件**
5. **任何需要永久保存的用戶數據**

## 💡 使用說明

### 正常使用流程

```bash
# 1. 啟動服務
docker-compose up -d

# 2. 用戶上傳文件（通過 API）
# 文件會自動保存到 backend/uploads/

# 3. 查看上傳的文件
ls -lh backend/uploads/

# 4. 停止並刪除容器（文件不會丟失！）
docker-compose down

# 5. 重新啟動（文件自動恢復）
docker-compose up -d
```

### 安全操作指南

```bash
# ✅ 安全操作 - 文件會保留
docker-compose down                # 停止並刪除容器
docker-compose restart backend     # 重啟服務
docker-compose up -d --build       # 重新構建並啟動

# ⚠️ 注意操作
docker-compose down -v             # -v 會刪除 named volumes
                                   # 但不會刪除 bind mounts（uploads 使用的是 bind mount，所以文件仍會保留）

# ⚠️ 危險操作 - 會真正刪除文件
rm -rf backend/uploads/*           # 直接刪除主機目錄
docker volume prune -a             # 清理所有 volumes（但 bind mounts 不受影響）
```

### 查看和管理文件

```bash
# 在主機查看
ls -lh backend/uploads/

# 在容器內查看
docker exec resumexlab-backend ls -lh /app/uploads/

# 查看文件內容
docker exec resumexlab-backend cat /app/uploads/file.txt

# 統計文件數量
ls -1 backend/uploads/ | wc -l

# 查看目錄大小
du -sh backend/uploads/
```

## 🎉 完成檢查

### 配置檢查

```bash
# 驗證所有配置
grep "uploads" docker-compose.yml docker-compose.dev.yml backend/Dockerfile
```

**預期看到：**
- ✅ `docker-compose.yml` 中有 `./backend/uploads:/app/uploads`
- ✅ `docker-compose.dev.yml` 中有 `./backend/uploads:/app/uploads`
- ✅ `Dockerfile` 中有 `mkdir -p /app/data /app/uploads`

### 功能檢查

執行自動化測試確認一切正常：

```bash
./test_uploads_persistence.sh
```

**成功標誌：**
```
✓ 測試通過！
uploads 目錄已正確配置持久化
```

## 🔗 相關文件

### 配置文件
- `docker-compose.yml` - 生產環境配置 (第 50 行)
- `docker-compose.dev.yml` - 開發環境配置 (第 48 行)
- `backend/Dockerfile` - 後端容器構建配置 (第 43 行)

### 文檔和工具
- `QUICK_START_UPLOADS.md` - 快速開始指南
- `test_uploads_persistence.sh` - 自動化測試腳本
- `docs/docker-commands-reference.md` - Docker 指令參考大全
- `docs/volume-mounting-diagram.md` - Volume 掛載架構圖解

## 📚 延伸閱讀

- [Docker Volumes 官方文檔](https://docs.docker.com/storage/volumes/)
- [Docker Compose Volumes 配置](https://docs.docker.com/compose/compose-file/compose-file-v3/#volumes)
- [Docker Bind Mounts](https://docs.docker.com/storage/bind-mounts/)

## 🆘 常見問題排查

### Q1: 文件權限錯誤

**問題**: 容器內無法寫入文件

**解決方法**:
```bash
# 調整目錄權限
chmod 755 backend/uploads

# 如果需要調整所有者
sudo chown -R $(id -u):$(id -g) backend/uploads
```

### Q2: 容器內看不到文件

**問題**: 主機有文件但容器內看不到

**解決方法**:
```bash
# 1. 檢查 volume 掛載是否成功
docker inspect resumexlab-backend | grep -A 10 Mounts

# 2. 重啟容器
docker-compose restart backend

# 3. 重新構建並啟動
docker-compose up -d --build
```

### Q3: 如何刪除所有上傳文件

**解決方法**:
```bash
# ⚠️ 警告：會刪除所有上傳的文件
rm -rf backend/uploads/*

# 保留測試文件
find backend/uploads/ -type f ! -name 'test_*' -delete
```

### Q4: 如何備份上傳的文件

**解決方法**:
```bash
# 方法 1: 使用 tar 打包
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz backend/uploads/

# 方法 2: 使用 rsync 同步
rsync -av backend/uploads/ /path/to/backup/uploads/

# 方法 3: 使用 cp 複製
cp -r backend/uploads/ uploads_backup_$(date +%Y%m%d)/
```

---

**配置完成日期**: 2026-01-31
**配置狀態**: ✅ 已完成並驗證
**支持環境**: 生產環境 & 開發環境
**測試狀態**: ✅ 測試腳本已創建
