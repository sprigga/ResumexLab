# Docker Compose 環境快速切換指南

## 📁 配置檔案說明

| 檔案 | 用途 | 前端端口 | 後端端口 |
|------|------|---------|---------|
| `docker-compose.yml` | **生產環境** (GCP VM) | 58432 | 58433 |
| `docker-compose.dev.yml` | **開發環境** (本地) | 8000 | 8001 |

---

## 🚀 快速開始

### 開發環境 (本地開發)

```bash
# 啟動開發環境
docker-compose -f docker-compose.dev.yml up -d --build

# 訪問
# 前端: http://localhost:8000
# 後端: http://localhost:8001/docs

# 停止
docker-compose -f docker-compose.dev.yml down
```

### 生產環境 (GCP VM)

```bash
# 啟動生產環境
docker-compose up -d --build

# 訪問
# 前端: http://<YOUR-IP>:58432
# 後端: http://<YOUR-IP>:58433/docs

# 停止
docker-compose down
```

---

## 🔄 環境切換

### 從開發環境切換到生產環境

```bash
# 1. 停止開發環境
docker-compose -f docker-compose.dev.yml down

# 2. 啟動生產環境
docker-compose up -d --build
```

### 從生產環境切換到開發環境

```bash
# 1. 停止生產環境
docker-compose down

# 2. 啟動開發環境
docker-compose -f docker-compose.dev.yml up -d --build
```

---

## 📋 常用命令

### 查看運行狀態

```bash
# 開發環境
docker-compose -f docker-compose.dev.yml ps

# 生產環境
docker-compose ps
```

### 查看日誌

```bash
# 開發環境
docker-compose -f docker-compose.dev.yml logs -f

# 生產環境
docker-compose logs -f
```

### 重新建置

```bash
# 開發環境
docker-compose -f docker-compose.dev.yml up -d --build

# 生產環境
docker-compose up -d --build
```

---

## ⚠️ 注意事項

1. **不要同時運行兩個環境** - 會導致端口衝突
2. **開發環境**: 使用非特權端口,不需要 sudo
3. **生產環境**: 使用高位端口,適合 GCP VM 部署
4. **資料庫**: 兩個環境共用同一個 `./backend/data` 目錄

---

## 🔧 故障排除

### 端口衝突

```bash
# 檢查端口佔用
sudo lsof -i :8000 -i :8001 -i :58432 -i :58433

# 停止所有容器
docker-compose -f docker-compose.dev.yml down
docker-compose down
```

### 清理所有環境

```bash
# 停止所有相關容器
docker stop $(docker ps -q --filter "name=resumexlab")

# 移除所有容器
docker rm $(docker ps -aq --filter "name=resumexlab")
```

---

## 📚 詳細文件

完整部署指南請參考: [`scripts/DEPLOYMENT_GUIDE.md`](./scripts/DEPLOYMENT_GUIDE.md)

---

**最後更新**: 2025-01-12
