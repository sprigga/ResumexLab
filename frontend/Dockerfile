# Frontend Dockerfile for Resume Management System
# 使用多階段構建來優化鏡像大小

# 第一階段：構建階段
FROM node:20-alpine AS builder

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝依賴
RUN npm ci

# 複製應用程式碼
COPY . .

# 增加 Node.js 記憶體限制並構建應用
RUN NODE_OPTIONS="--max-old-space-size=1024" npm run build

# 構建應用
RUN npm run build

# 第二階段：生產階段（使用 nginx）
FROM nginx:alpine

# 複製自定義 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 從構建階段複製構建產物到 nginx 的靜態文件目錄
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 啟動 nginx
CMD ["nginx", "-g", "daemon off;"]
