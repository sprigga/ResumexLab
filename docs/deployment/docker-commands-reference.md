# Docker 常用指令參考

## 📦 容器管理

### 啟動服務

```bash
# 啟動所有服務（生產環境）
docker-compose up -d

# 啟動所有服務（開發環境）
docker-compose -f docker-compose.dev.yml up -d

# 啟動並重新構建
docker-compose up -d --build

# 僅啟動 backend
docker-compose up -d backend

# 僅啟動 frontend
docker-compose up -d frontend
```

### 停止服務

```bash
# 停止所有服務（保留容器）
docker-compose stop

# 停止並刪除容器（保留 volumes）
docker-compose down

# 停止並刪除容器和 volumes（⚠️ 會刪除數據）
docker-compose down -v

# 停止並刪除容器、volumes 和鏡像
docker-compose down -v --rmi all
```

### 重啟服務

```bash
# 重啟所有服務
docker-compose restart

# 重啟 backend
docker-compose restart backend

# 重啟 frontend
docker-compose restart frontend
```

## 🔍 查看狀態

### 容器狀態

```bash
# 查看所有運行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看特定項目的容器
docker-compose ps

# 查看容器資源使用
docker stats

# 查看特定容器資源使用
docker stats resumexlab-backend
```

### 日誌查看

```bash
# 查看所有服務日誌
docker-compose logs

# 實時查看日誌
docker-compose logs -f

# 查看 backend 日誌
docker-compose logs backend

# 實時查看 backend 日誌
docker-compose logs -f backend

# 查看最近 100 行日誌
docker-compose logs --tail 100 backend

# 查看特定容器日誌
docker logs resumexlab-backend

# 實時查看特定容器日誌
docker logs -f resumexlab-backend
```

## 🖥️ 進入容器

### 互動式 Shell

```bash
# 使用 bash 進入 backend 容器
docker exec -it resumexlab-backend /bin/bash

# 如果沒有 bash，使用 sh
docker exec -it resumexlab-backend /bin/sh

# 使用 docker-compose
docker-compose exec backend /bin/bash

# 進入 frontend 容器
docker exec -it resumexlab-frontend /bin/bash
```

### 執行單一命令

```bash
# 查看容器內目錄
docker exec resumexlab-backend ls -la /app

# 查看 uploads 目錄
docker exec resumexlab-backend ls -la /app/uploads

# 查看環境變數
docker exec resumexlab-backend env

# 測試 API 健康檢查
docker exec resumexlab-backend curl -f http://localhost:8000/health

# 查看資料庫文件
docker exec resumexlab-backend ls -la /app/data
```

## 📂 文件操作

### 複製文件

```bash
# 從容器複製文件到主機
docker cp resumexlab-backend:/app/data/resume.db ./backup.db

# 從主機複製文件到容器
docker cp ./config.json resumexlab-backend:/app/config.json

# 複製整個目錄
docker cp resumexlab-backend:/app/uploads ./uploads_backup
```

### Volume 管理

```bash
# 列出所有 volumes
docker volume ls

# 查看 volume 詳細資訊
docker volume inspect <volume_name>

# 刪除未使用的 volumes
docker volume prune

# 刪除特定 volume
docker volume rm <volume_name>
```

## 🏗️ 構建與鏡像

### 構建鏡像

```bash
# 構建所有服務
docker-compose build

# 構建特定服務
docker-compose build backend

# 不使用緩存構建
docker-compose build --no-cache

# 構建並啟動
docker-compose up -d --build
```

### 鏡像管理

```bash
# 列出所有鏡像
docker images

# 刪除特定鏡像
docker rmi <image_id>

# 刪除未使用的鏡像
docker image prune

# 刪除所有未使用的鏡像
docker image prune -a

# 查看鏡像詳細資訊
docker inspect <image_id>
```

## 🔧 維護與清理

### 系統清理

```bash
# 清理未使用的容器、網路、鏡像（保留 volumes）
docker system prune

# 清理所有未使用的資源（包括 volumes）⚠️
docker system prune -a --volumes

# 查看 Docker 佔用空間
docker system df

# 查看詳細空間使用
docker system df -v
```

### 特定清理

```bash
# 停止所有容器
docker stop $(docker ps -a -q)

# 刪除所有停止的容器
docker container prune

# 刪除所有未使用的網路
docker network prune

# 刪除特定容器
docker rm resumexlab-backend
```

## 🔍 診斷與偵錯

### 容器診斷

```bash
# 查看容器詳細資訊
docker inspect resumexlab-backend

# 查看容器進程
docker top resumexlab-backend

# 查看容器內部網路
docker exec resumexlab-backend ip addr

# 查看容器內部進程
docker exec resumexlab-backend ps aux

# 測試容器間網路連接
docker exec resumexlab-backend ping frontend
```

### 健康檢查

```bash
# 查看容器健康狀態
docker inspect --format='{{.State.Health.Status}}' resumexlab-backend

# 查看健康檢查日誌
docker inspect --format='{{json .State.Health}}' resumexlab-backend | jq
```

## 🌐 網路管理

### 網路操作

```bash
# 列出所有網路
docker network ls

# 查看網路詳細資訊
docker network inspect resumexlab-network

# 創建網路
docker network create my-network

# 刪除網路
docker network rm resumexlab-network

# 連接容器到網路
docker network connect resumexlab-network <container_name>

# 斷開容器與網路
docker network disconnect resumexlab-network <container_name>
```

## 📊 資料庫相關

### SQLite 操作

```bash
# 進入容器並操作資料庫
docker exec -it resumexlab-backend /bin/bash

# 在容器內執行 SQLite
sqlite3 /app/data/resume.db

# 直接從主機操作（如果有 sqlite3）
sqlite3 backend/data/resume.db

# 查看資料庫表
docker exec resumexlab-backend sqlite3 /app/data/resume.db ".tables"

# 導出資料庫
docker exec resumexlab-backend sqlite3 /app/data/resume.db ".dump" > backup.sql

# 備份資料庫文件
docker cp resumexlab-backend:/app/data/resume.db ./backup_$(date +%Y%m%d).db
```

## 🚀 開發工作流程

### 完整重啟流程

```bash
# 1. 停止並刪除容器
docker-compose down

# 2. 重新構建鏡像
docker-compose build --no-cache

# 3. 啟動服務
docker-compose up -d

# 4. 查看日誌確認啟動成功
docker-compose logs -f
```

### 快速更新流程

```bash
# 1. 僅重新構建並重啟
docker-compose up -d --build

# 2. 查看日誌
docker-compose logs -f backend
```

### 測試持久化流程

```bash
# 1. 創建測試文件
echo "test" > backend/uploads/test.txt

# 2. 啟動容器
docker-compose up -d

# 3. 驗證文件存在
docker exec resumexlab-backend cat /app/uploads/test.txt

# 4. 刪除容器
docker-compose down

# 5. 驗證文件仍在主機
cat backend/uploads/test.txt

# 6. 重新啟動
docker-compose up -d

# 7. 驗證文件在新容器中可訪問
docker exec resumexlab-backend cat /app/uploads/test.txt
```

## 🎯 常用組合指令

### 完全重置

```bash
# ⚠️ 警告：會刪除所有數據
docker-compose down -v --rmi all
docker system prune -a --volumes
```

### 保留數據重置

```bash
# 僅重置容器和鏡像，保留 volumes
docker-compose down --rmi all
docker-compose build --no-cache
docker-compose up -d
```

### 生產部署更新

```bash
# 拉取最新代碼
git pull

# 重新構建並啟動（不中斷服務）
docker-compose up -d --build --no-deps backend

# 查看日誌確認
docker-compose logs -f backend
```

## 📖 參考資料

- [Docker 官方文檔](https://docs.docker.com/)
- [Docker Compose 文檔](https://docs.docker.com/compose/)
- [Docker CLI 參考](https://docs.docker.com/engine/reference/commandline/cli/)

---

**最後更新**: 2026-01-31
