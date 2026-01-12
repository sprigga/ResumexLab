#!/bin/bash
# API 測試腳本
# 已建立於 2025-01-12，原因：測試 API 端點是否正確處理空資料的情況

echo "=========================================="
echo "測試 API 端點處理空資料的情況"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000/api"

echo "1. 測試 GET /api/personal-info/"
echo "預期: 回傳空物件或預設物件,而不是 404 錯誤"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/personal-info/"
echo ""
echo "----------------------------------------"
echo ""

echo "2. 測試 GET /api/work-experience/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/work-experience/"
echo ""
echo "----------------------------------------"
echo ""

echo "3. 測試 GET /api/projects/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/projects/"
echo ""
echo "----------------------------------------"
echo ""

echo "4. 測試 GET /api/education/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/education/"
echo ""
echo "----------------------------------------"
echo ""

echo "5. 測試 GET /api/certifications/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/certifications/"
echo ""
echo "----------------------------------------"
echo ""

echo "6. 測試 GET /api/languages/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/languages/"
echo ""
echo "----------------------------------------"
echo ""

echo "7. 測試 GET /api/publications/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/publications/"
echo ""
echo "----------------------------------------"
echo ""

echo "8. 測試 GET /api/github-projects/"
echo "預期: 回傳空陣列 []"
curl -s -w "\nHTTP 狀態碼: %{http_code}\n" "$BASE_URL/github-projects/"
echo ""
echo "=========================================="
echo "測試完成"
echo "=========================================="
