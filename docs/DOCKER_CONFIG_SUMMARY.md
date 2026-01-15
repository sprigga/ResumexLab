# Docker Compose 配置總結

## 📁 配置檔案

| 檔案 | 環境 | 前端端口 | 後端端口 | 用途 |
|------|------|---------|---------|------|
| `docker-compose.yml` | 生產 (GCP VM) | 58432 | 58433 | GCP VM 部署 |
| `docker-compose.dev.yml` | 開發 (本地) | 8000 | 8001 | 本地開發 |

## 🚀 快速指令

### 開發環境
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 生產環境
```bash
docker-compose up -d
```

### 查看狀態
```bash
# 開發
docker-compose -f docker-compose.dev.yml ps

# 生產
docker-compose ps
```

### 查看日誌
```bash
# 開發
docker-compose -f docker-compose.dev.yml logs -f

# 生產
docker-compose logs -f
```

### 停止服務
```bash
# 開發
docker-compose -f docker-compose.dev.yml down

# 生產
docker-compose down
```

## 🔗 訪問地址

### 開發環境
- 前端: http://localhost:8000
- 後端 API: http://localhost:8001/api
- API 文件: http://localhost:8001/docs

### 生產環境 (GCP VM)
- 前端: http://<YOUR-IP>:58432
- 後端 API: http://<YOUR-IP>:58433/api
- API 文件: http://<YOUR-IP>:58433/docs

## 📚 詳細文件

- [快速切換指南](./DOCKER_COMPOSE_USAGE.md)
- [完整部署指南](./scripts/DEPLOYMENT_GUIDE.md)

---
**建立日期**: 2025-01-12
