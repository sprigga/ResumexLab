#!/bin/bash
# 測試 uploads 目錄持久化腳本
# 用途: 驗證 docker-compose down 後 uploads 目錄內的文件是否保留

set -e

echo "==================================="
echo "測試 uploads 目錄持久化"
echo "==================================="

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 確保 uploads 目錄存在
echo -e "\n${YELLOW}步驟 1: 確認 uploads 目錄存在${NC}"
if [ ! -d "backend/uploads" ]; then
    mkdir -p backend/uploads
    echo "✓ 已創建 backend/uploads 目錄"
else
    echo "✓ backend/uploads 目錄已存在"
fi

# 2. 創建測試文件
echo -e "\n${YELLOW}步驟 2: 創建測試文件${NC}"
TEST_FILE="backend/uploads/test_persistence_$(date +%Y%m%d_%H%M%S).txt"
echo "這是一個測試文件，用於驗證 docker-compose down 後文件是否保留" > "$TEST_FILE"
echo "創建時間: $(date)" >> "$TEST_FILE"
echo "✓ 已創建測試文件: $TEST_FILE"

# 3. 列出當前文件
echo -e "\n${YELLOW}步驟 3: 列出當前 uploads 目錄內容${NC}"
ls -lh backend/uploads/
FILE_COUNT_BEFORE=$(ls -1 backend/uploads/ | wc -l)
echo "文件數量: $FILE_COUNT_BEFORE"

# 4. 啟動容器
echo -e "\n${YELLOW}步驟 4: 啟動 Docker 容器${NC}"
docker-compose up -d backend
echo "✓ 容器已啟動，等待 5 秒..."
sleep 5

# 5. 驗證容器內的文件
echo -e "\n${YELLOW}步驟 5: 檢查容器內 uploads 目錄${NC}"
docker exec resumexlab-backend ls -lh /app/uploads/
CONTAINER_FILE_COUNT=$(docker exec resumexlab-backend ls -1 /app/uploads/ | wc -l)
echo "容器內文件數量: $CONTAINER_FILE_COUNT"

# 6. 停止並刪除容器
echo -e "\n${YELLOW}步驟 6: 執行 docker-compose down${NC}"
docker-compose down
echo "✓ 容器已刪除"

# 7. 驗證主機文件是否保留
echo -e "\n${YELLOW}步驟 7: 驗證主機上的文件是否保留${NC}"
if [ -f "$TEST_FILE" ]; then
    echo -e "${GREEN}✓ 成功！測試文件仍然存在${NC}"
    echo "文件內容:"
    cat "$TEST_FILE"
else
    echo -e "${RED}✗ 失敗！測試文件已消失${NC}"
    exit 1
fi

FILE_COUNT_AFTER=$(ls -1 backend/uploads/ | wc -l)
echo -e "\ndocker-compose down 前文件數: $FILE_COUNT_BEFORE"
echo "docker-compose down 後文件數: $FILE_COUNT_AFTER"

if [ "$FILE_COUNT_BEFORE" -eq "$FILE_COUNT_AFTER" ]; then
    echo -e "\n${GREEN}==================================="
    echo "✓ 測試通過！"
    echo "uploads 目錄已正確配置持久化"
    echo "===================================${NC}"
else
    echo -e "\n${RED}==================================="
    echo "✗ 測試失敗！"
    echo "文件數量不一致"
    echo "===================================${NC}"
    exit 1
fi
