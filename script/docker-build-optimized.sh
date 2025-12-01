#!/bin/bash
# Docker 構建優化腳本
# 日期: 2025-12-01
# 功能: 提供多種鏡像源選擇進行 Docker 構建

set -e  # 遇到錯誤時退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Docker 構建優化腳本 ===${NC}"
echo ""
echo "請選擇要使用的鏡像源:"
echo "1) 阿里雲鏡像 (Aliyun) - 適合中國大陸地區"
echo "2) 清華大學鏡像 (Tsinghua) - 適合中國大陸地區"
echo "3) 中科大鏡像 (USTC) - 適合中國大陸地區"
echo "4) 官方源 (Official) - 適合海外地區"
echo ""
read -p "輸入選項 (1-4): " choice

case $choice in
    1)
        echo -e "${YELLOW}使用阿里雲鏡像進行構建...${NC}"
        DOCKERFILE="Dockerfile"
        ;;
    2)
        echo -e "${YELLOW}使用清華大學鏡像進行構建...${NC}"
        DOCKERFILE="Dockerfile.tsinghua"
        ;;
    3)
        echo -e "${YELLOW}使用中科大鏡像進行構建...${NC}"
        DOCKERFILE="Dockerfile.ustc"
        ;;
    4)
        echo -e "${YELLOW}使用官方源進行構建...${NC}"
        # 創建臨時 Dockerfile 使用官方源
        cat > /tmp/Dockerfile.official << 'EOF'
FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends gcc curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
        DOCKERFILE="/tmp/Dockerfile.official"
        ;;
    *)
        echo -e "${RED}無效的選項!${NC}"
        exit 1
        ;;
esac

# 切換到 backend 目錄
cd "$(dirname "$0")/../backend" || exit 1

# 開始構建
echo -e "${GREEN}開始構建 Docker 鏡像...${NC}"
echo "Dockerfile: $DOCKERFILE"
echo ""

# 構建命令
docker build -f "$DOCKERFILE" -t resumexlab-backend:latest .

# 檢查構建結果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ 構建成功!${NC}"
    echo ""
    echo "可使用以下命令測試:"
    echo "  docker run -p 58433:8000 resumexlab-backend:latest"
else
    echo ""
    echo -e "${RED}✗ 構建失敗!${NC}"
    exit 1
fi
