#!/bin/bash
# API 逾時測試腳本
# 已建立於 2025-01-12，原因：測試 API 回應時間,檢查是否有逾時問題

echo "=========================================="
echo "API 回應時間測試"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000/api"

# 測試每個 API 的回應時間
test_api() {
    local api_name=$1
    local api_url=$2

    echo "測試: $api_name"
    echo "URL: $api_url"

    # 使用 time 測量實際回應時間,curl 測量 HTTP 狀態
    response_time=$(curl -o /dev/null -s -w "%{time_total}\n" "$api_url")
    http_code=$(curl -o /dev/null -s -w "%{http_code}\n" "$api_url")

    echo "HTTP 狀態碼: $http_code"
    echo "回應時間: ${response_time} 秒"

    # 檢查是否超過 5 秒
    if (( $(echo "$response_time > 5.0" | bc -l) )); then
        echo "⚠️  警告: 回應時間超過 5 秒"
    fi

    # 檢查是否超過 10 秒
    if (( $(echo "$response_time > 10.0" | bc -l) )); then
        echo "❌ 嚴重警告: 回應時間超過 10 秒"
    fi

    echo "----------------------------------------"
    echo ""
}

# 依序測試所有 API
test_api "個人資訊" "$BASE_URL/personal-info/"
test_api "工作經歷" "$BASE_URL/work-experience/"
test_api "專案經驗" "$BASE_URL/projects/"
test_api "教育背景" "$BASE_URL/education/"
test_api "證照" "$BASE_URL/certifications/"
test_api "語言能力" "$BASE_URL/languages/"
test_api "學術著作" "$BASE_URL/publications/"
test_api "GitHub 專案" "$BASE_URL/github-projects/"

echo "=========================================="
echo "測試完成"
echo "=========================================="
echo ""
echo "說明:"
echo "- 如果所有 API 回應時間都 < 1 秒: 正常"
echo "- 如果有 API 回應時間 > 5 秒: 需要檢查效能"
echo "- 如果有 API 回應時間 > 10 秒: 可能需要優化資料庫查詢"
