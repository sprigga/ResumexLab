#!/bin/bash

echo "=== 檢查剪貼簿內容 ==="
osascript -e 'clipboard info'

echo -e "\n=== 測試貼上圖片 ==="
TEST_IMAGE="/Users/pololin/python_project/resumexlab/.cp-images/test-paste.png"

if pngpaste "$TEST_IMAGE" 2>/dev/null; then
    echo "✓ 圖片貼上成功！"
    echo "檔案大小: $(du -h "$TEST_IMAGE" | cut -f1)"
    ls -lh "$TEST_IMAGE"
else
    echo "✗ 貼上失敗 - 請先複製一張圖片到剪貼簿"
    echo ""
    echo "如何複製圖片："
    echo "1. 按 Cmd+Shift+4 截圖（會自動複製）"
    echo "2. 或在圖片上右鍵 → 複製圖片"
fi
