# Docker 部署說明

## 專案架構

此專案使用 Docker Compose 編排以下服務：

- **Frontend**: Vue.js 3 + Nginx (Port 80)
- **Backend**: FastAPI (Port 8000)
- **Database**: SQLite (持久化存儲)

## 文件說明

### Docker 相關文件

```
resumexlab/
├── docker-compose.yml          # Docker Compose 主配置文件
├── backend/
│   ├── Dockerfile             # 後端 Docker 鏡像配置
│   └── .dockerignore          # 後端 Docker 忽略文件
└── frontend/
    ├── Dockerfile             # 前端 Docker 鏡像配置
    ├── nginx.conf             # Nginx 配置文件
    └── .dockerignore          # 前端 Docker 忽略文件
```

## 快速開始

### 1. 前置需求

確保已安裝以下工具：
- Docker (>= 20.10)
- Docker Compose (>= 1.29)

### 2. 環境變數配置

在正式環境部署前，請修改 `docker-compose.yml` 中的環境變數：

```yaml
# 重要：請修改以下安全相關設定
- SECRET_KEY=your-secret-key-change-this-in-production  # 修改為隨機字串
- BACKEND_CORS_ORIGINS=["http://localhost","http://your-domain.com"]
```

### 3. 構建並啟動服務

#### 完整啟動（構建 + 啟動）

```bash
# 在專案根目錄執行
docker-compose up --build
```

#### 背景運行

```bash
docker-compose up -d --build
```

#### 僅構建鏡像

```bash
docker-compose build
```

### 4. 驗證服務

服務啟動後，可以通過以下方式驗證：

- **前端**: http://localhost
- **後端 API**: http://localhost:8000
- **API 文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/health

### 5. 停止服務

```bash
# 停止服務（保留容器）
docker-compose stop

# 停止並移除容器
docker-compose down

# 停止並移除容器、網路、數據卷
docker-compose down -v
```

## 常用指令

### 查看日誌

```bash
# 查看所有服務日誌
docker-compose logs

# 查看特定服務日誌
docker-compose logs backend
docker-compose logs frontend

# 實時追蹤日誌
docker-compose logs -f
```

### 進入容器

```bash
# 進入後端容器
docker-compose exec backend sh

# 進入前端容器
docker-compose exec frontend sh
```

### 重啟服務

```bash
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart backend
docker-compose restart frontend
```

### 查看運行狀態

```bash
docker-compose ps
```

## 數據持久化

### SQLite 資料庫

資料庫文件存儲在 `./backend/data/resume.db`，通過 Docker volume 掛載確保數據持久化。

```yaml
volumes:
  - ./backend/data:/app/data
```

即使容器被刪除，資料庫文件仍會保留在主機上。

## Nginx 配置說明

前端使用 Nginx 作為 Web 伺服器，主要功能：

1. **靜態文件服務**: 提供 Vue.js 構建產物
2. **API 代理**: 將 `/api` 請求代理到後端服務
3. **Vue Router 支援**: 配置 `try_files` 支援 history mode
4. **Gzip 壓縮**: 優化傳輸效能
5. **快取控制**: 靜態資源長期快取

## 開發模式

### 本地開發（不使用 Docker）

```bash
# 後端
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

# 前端
cd frontend
npm run dev
```

### 開發模式 Docker（支援熱重載）

可以在 `docker-compose.yml` 中取消註解以下配置：

```yaml
backend:
  volumes:
    - ./backend/app:/app/app  # 掛載程式碼，支援熱重載
```

## 生產環境部署建議

### 1. 安全設定

- 修改 `SECRET_KEY` 為強隨機字串
- 設定正確的 `BACKEND_CORS_ORIGINS`
- 使用環境變數文件（.env）管理敏感資訊
- 關閉 DEBUG 模式

### 2. 效能優化

- 使用 `gunicorn` 替代 `uvicorn` 作為 WSGI 伺服器
- 配置 worker 數量：`--workers 4`
- 啟用 HTTP/2 (需要 HTTPS)

### 3. 資料庫遷移

對於大型應用，建議從 SQLite 遷移到 PostgreSQL：

```yaml
# 新增 PostgreSQL 服務
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: resumedb
    POSTGRES_USER: resumeuser
    POSTGRES_PASSWORD: changeme
  volumes:
    - postgres-data:/var/lib/postgresql/data
```

### 4. HTTPS 配置

使用 Let's Encrypt + Certbot 配置 SSL 證書：

```bash
# 安裝 certbot
docker-compose run --rm certbot certonly --webroot \
  -w /var/www/certbot \
  -d your-domain.com
```

### 5. 反向代理（推薦）

在生產環境建議在前面加一層 Nginx 或 Traefik 作為反向代理，處理：
- SSL/TLS 終止
- 負載均衡
- 請求限流
- 安全標頭

## 疑難排解

### 問題 1: 容器無法啟動

```bash
# 查看詳細錯誤日誌
docker-compose logs backend
docker-compose logs frontend
```

### 問題 2: 端口衝突

如果 80 或 8000 端口被占用，修改 `docker-compose.yml`：

```yaml
ports:
  - "8080:80"   # 改為 8080
  - "8001:8000" # 改為 8001
```

### 問題 3: 前端無法連接後端

1. 檢查 `frontend/nginx.conf` 中的代理配置
2. 確認後端服務名稱為 `backend`
3. 檢查網路配置：`docker network ls`

### 問題 4: 資料庫文件權限問題

```bash
# 修正權限
sudo chown -R $USER:$USER ./backend/data
chmod -R 755 ./backend/data
```

## 維護建議

### 定期備份

```bash
# 備份資料庫
cp ./backend/data/resume.db ./backup/resume_$(date +%Y%m%d).db

# 使用腳本自動備份
#!/bin/bash
BACKUP_DIR="./backup"
mkdir -p $BACKUP_DIR
cp ./backend/data/resume.db "$BACKUP_DIR/resume_$(date +%Y%m%d_%H%M%S).db"
echo "Backup completed!"
```

### 清理未使用的鏡像

```bash
# 清理未使用的鏡像
docker image prune

# 清理所有未使用的資源
docker system prune -a
```

### 更新鏡像

```bash
# 重新構建並啟動
docker-compose up -d --build

# 拉取最新基礎鏡像
docker-compose pull
docker-compose up -d --build
```

## 參考資源

- [Docker 官方文檔](https://docs.docker.com/)
- [Docker Compose 文檔](https://docs.docker.com/compose/)
- [Nginx 官方文檔](https://nginx.org/en/docs/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [Vue.js 部署指南](https://vuejs.org/guide/best-practices/production-deployment.html)
