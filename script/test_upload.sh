#!/bin/bash
# 快速測試檔案上傳功能
# Created on 2025-01-12
# Purpose: Quick test for file upload functionality

echo "測試上傳功能..."

# 先登入取得 token
echo "步驟 1: 登入..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:58433/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ 登入失敗"
    echo "回應: $LOGIN_RESPONSE"
    exit 1
fi

echo "✓ 登入成功"

# 建立一個測試檔案（1MB）
echo "步驟 2: 建立測試檔案（1MB）..."
dd if=/dev/zero of=/tmp/test_1mb.txt bs=1048576 count=1 2>/dev/null
echo "✓ 測試檔案建立完成"

# 測試上傳 1MB 檔案
echo "步驟 3: 測試上傳 1MB 檔案..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:58433/api/projects/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_1mb.txt" \
  -F "title_zh=測試專案" \
  -F "title_en=Test Project" \
  -F "display_order=0")

HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ 1MB 檔案上傳成功"
elif [ "$HTTP_CODE" = "413" ]; then
    echo "❌ 收到 413 錯誤 - 需要重建 Docker 容器"
else
    echo "⚠️  收到狀態碼: $HTTP_CODE"
    echo "回應: $BODY"
fi

# 清理
rm -f /tmp/test_1mb.txt

# 如果要測試大檔案，建立 50MB 檔案
echo ""
echo "是否要測試 50MB 大檔案？(y/n)"
read -r answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo "步驟 4: 建立測試檔案（50MB）..."
    dd if=/dev/zero of=/tmp/test_50mb.txt bs=1048576 count=50 2>/dev/null
    echo "✓ 測試檔案建立完成"

    echo "步驟 5: 測試上傳 50MB 檔案..."
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:58433/api/projects/upload" \
      -H "Authorization: Bearer $TOKEN" \
      -F "file=@/tmp/test_50mb.txt" \
      -F "title_zh=大檔案測試專案" \
      -F "title_en=Large File Test Project" \
      -F "display_order=0" \
      --max-time 300)

    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "200" ]; then
        echo "✓ 50MB 檔案上傳成功！修復有效！"
    elif [ "$HTTP_CODE" = "413" ]; then
        echo "❌ 收到 413 錯誤 - 需要重建 Docker 容器"
        echo "請執行: ./script/rebuild_and_restart_docker.sh"
    else
        echo "⚠️  收到狀態碼: $HTTP_CODE"
        echo "回應: $BODY"
    fi

    # 清理
    rm -f /tmp/test_50mb.txt
fi

echo ""
echo "測試完成！"
