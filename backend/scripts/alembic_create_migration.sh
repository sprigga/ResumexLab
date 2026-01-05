#!/bin/bash
# Alembic 遷移創建腳本
#
# 此腳本自動化 Alembic 遷移創建流程，包含：
# 1. 健康檢查
# 2. 資料庫備份
# 3. 生成遷移
# 4. 檢查 SQLite 兼容性
# 5. 應用遷移（可選）
#
# 使用方法：
#   ./alembic_create_migration.sh "遷移描述"
#   ./alembic_create_migration.sh "遷移描述" --apply
#
# 作者: Polo (林鴻全)
# 日期: 2026-01-04

set -e  # 遇到錯誤立即退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# 輸出函數
print_header() {
    echo -e "\n${BLUE}${BOLD}================================================${NC}"
    echo -e "${BLUE}${BOLD}  $1${NC}"
    echo -e "${BLUE}${BOLD}================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# 檢查參數
if [ $# -lt 1 ]; then
    print_error "缺少遷移描述參數"
    echo ""
    echo "使用方法："
    echo "  ./alembic_create_migration.sh \"遷移描述\""
    echo "  ./alembic_create_migration.sh \"遷移描述\" --apply"
    echo ""
    echo "範例："
    echo "  ./alembic_create_migration.sh \"新增使用者頭像欄位\""
    echo "  ./alembic_create_migration.sh \"新增使用者頭像欄位\" --apply"
    exit 1
fi

MIGRATION_MESSAGE="$1"
AUTO_APPLY=false

# 檢查是否要自動應用
if [ "$2" == "--apply" ]; then
    AUTO_APPLY=true
fi

# 取得腳本所在目錄
# 原本路徑邏輯 (已註解於 2026-01-04，原因：腳本移動到 backend/scripts/)
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# BACKEND_DIR="$PROJECT_ROOT/backend"

# 新路徑邏輯 (修改於 2026-01-04，原因：腳本現在位於 backend/scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # backend/scripts/
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"                          # backend/
PROJECT_ROOT="$(dirname "$BACKEND_DIR")"                        # project root

# 切換到 backend 目錄
cd "$BACKEND_DIR"

print_header "Alembic 遷移創建助手"
print_info "遷移描述: $MIGRATION_MESSAGE"

# 1. 健康檢查
print_header "步驟 1: 環境檢查"

# 原本虛擬環境檢查 - 已註解於 2026-01-05
# 原因: 改為檢查 Python 環境，而非檢查特定虛擬環境目錄
# if [ ! -d ".venv" ]; then
#     print_error "找不到虛擬環境 (.venv)"
#     exit 1
# fi
# print_success "虛擬環境存在"

# 新 Python 環境檢查 - 修改於 2026-01-05
# 原因: 改為檢查 Python 是否可用，支援多種 Python 環境管理方式
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    print_error "找不到 Python 環境"
    print_info "請確保 Python 已安裝並在 PATH 中"
    exit 1
fi

# 取得 Python 版本資訊
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    PYTHON_CMD="python"
else
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_CMD="python3"
fi

print_success "Python 環境存在: $PYTHON_CMD $PYTHON_VERSION"

# 檢查 alembic.ini
if [ ! -f "alembic.ini" ]; then
    print_error "找不到 alembic.ini"
    exit 1
fi
print_success "Alembic 配置存在"

# 檢查資料庫
if [ ! -f "data/resume.db" ]; then
    print_warning "資料庫不存在，將在首次遷移時創建"
else
    print_success "資料庫存在"
    # 顯示資料庫大小
    DB_SIZE=$(du -h data/resume.db | cut -f1)
    print_info "資料庫大小: $DB_SIZE"
fi

# 啟動虛擬環境
# source .venv/bin/activate

# 2. 檢查當前版本
print_header "步驟 2: 檢查當前版本"

CURRENT_VERSION=$(alembic current 2>&1 | grep -v "^INFO" | head -1)
if [ -z "$CURRENT_VERSION" ]; then
    print_warning "資料庫尚未標記版本"
    print_info "如果資料庫已有表結構，請先執行: alembic stamp head"
else
    print_success "當前版本: $CURRENT_VERSION"
fi

# 3. 備份資料庫
if [ -f "data/resume.db" ]; then
    print_header "步驟 3: 備份資料庫"

    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="data/resume_backup_${TIMESTAMP}.db"

    cp data/resume.db "$BACKUP_FILE"
    print_success "備份完成: $BACKUP_FILE"

    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    print_info "備份大小: $BACKUP_SIZE"
else
    print_info "資料庫不存在，跳過備份"
fi

# 4. 生成遷移
print_header "步驟 4: 生成遷移檔案"

print_info "執行: alembic revision --autogenerate -m \"$MIGRATION_MESSAGE\""

# 執行並捕獲輸出
MIGRATION_OUTPUT=$(alembic revision --autogenerate -m "$MIGRATION_MESSAGE" 2>&1)
MIGRATION_STATUS=$?

# 顯示輸出
echo "$MIGRATION_OUTPUT"

if [ $MIGRATION_STATUS -ne 0 ]; then
    print_error "遷移生成失敗"
    exit 1
fi

# 提取生成的檔案路徑
MIGRATION_FILE=$(echo "$MIGRATION_OUTPUT" | grep "Generating" | sed 's/Generating //' | sed 's/ \.\.\..*//')

if [ -z "$MIGRATION_FILE" ]; then
    print_error "無法找到生成的遷移檔案"
    exit 1
fi

print_success "遷移檔案已生成: $MIGRATION_FILE"

# 5. 檢查 SQLite 兼容性
print_header "步驟 5: 檢查 SQLite 兼容性"

if grep -q "op.alter_column" "$MIGRATION_FILE"; then
    print_warning "偵測到 SQLite 不支援的 ALTER COLUMN 操作！"
    print_info "SQLite 限制："
    print_info "  ✗ ALTER COLUMN (修改欄位)"
    print_info "  ✗ DROP CONSTRAINT"
    print_info "  ✓ ADD COLUMN (新增欄位)"
    print_info "  ✓ DROP COLUMN (刪除欄位, SQLite 3.35.0+)"

    echo ""
    print_warning "發現以下 ALTER COLUMN 操作："
    grep -n "op.alter_column" "$MIGRATION_FILE" | while read line; do
        echo "  $line"
    done

    echo ""
    print_info "建議操作："
    print_info "  1. 使用腳本自動修復: python scripts/alembic_helper.py fix-sqlite"
    print_info "  2. 手動編輯檔案，註解掉 alter_column 相關行"
    print_info "  3. 使用表重建策略（適用於複雜變更）"

    echo ""
    read -p "是否使用自動修復? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "執行自動修復..."
        python scripts/alembic_helper.py fix-sqlite

        if [ $? -eq 0 ]; then
            print_success "自動修復完成"
        else
            print_error "自動修復失敗"
            exit 1
        fi
    else
        print_warning "請手動修復後再執行遷移"
        AUTO_APPLY=false
    fi
else
    print_success "未發現兼容性問題"
fi

# 6. 顯示遷移內容摘要
print_header "步驟 6: 遷移內容摘要"

# 統計變更
ADD_COLUMN_COUNT=$(grep -c "op.add_column" "$MIGRATION_FILE" || true)
DROP_COLUMN_COUNT=$(grep -c "op.drop_column" "$MIGRATION_FILE" || true)
CREATE_TABLE_COUNT=$(grep -c "op.create_table" "$MIGRATION_FILE" || true)
DROP_TABLE_COUNT=$(grep -c "op.drop_table" "$MIGRATION_FILE" || true)
ALTER_COLUMN_COUNT=$(grep -c "op.alter_column" "$MIGRATION_FILE" || true)

echo "檢測到的變更："
[ $CREATE_TABLE_COUNT -gt 0 ] && print_info "  建立表: $CREATE_TABLE_COUNT 個"
[ $DROP_TABLE_COUNT -gt 0 ] && print_info "  刪除表: $DROP_TABLE_COUNT 個"
[ $ADD_COLUMN_COUNT -gt 0 ] && print_info "  新增欄位: $ADD_COLUMN_COUNT 個"
[ $DROP_COLUMN_COUNT -gt 0 ] && print_info "  刪除欄位: $DROP_COLUMN_COUNT 個"
[ $ALTER_COLUMN_COUNT -gt 0 ] && print_warning "  修改欄位: $ALTER_COLUMN_COUNT 個 (已註解)"

if [ $CREATE_TABLE_COUNT -eq 0 ] && [ $DROP_TABLE_COUNT -eq 0 ] && \
   [ $ADD_COLUMN_COUNT -eq 0 ] && [ $DROP_COLUMN_COUNT -eq 0 ] && \
   [ $ALTER_COLUMN_COUNT -eq 0 ]; then
    print_warning "沒有偵測到模型變更"
    print_info "可能原因："
    print_info "  1. 模型未修改"
    print_info "  2. alembic/env.py 中的 target_metadata 設定不正確"
    print_info "  3. Python cache 需要清除"
fi

# 7. 應用遷移（可選）
if [ "$AUTO_APPLY" = true ]; then
    print_header "步驟 7: 應用遷移"

    print_warning "即將應用遷移到資料庫"
    read -p "確定要繼續嗎? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "執行: alembic upgrade head"

        alembic upgrade head

        if [ $? -eq 0 ]; then
            print_success "遷移應用成功"

            # 顯示當前版本
            echo ""
            print_info "當前版本:"
            alembic current
        else
            print_error "遷移應用失敗"

            if [ -f "$BACKUP_FILE" ]; then
                print_info "可使用備份恢復: $BACKUP_FILE"
            fi

            exit 1
        fi
    else
        print_info "跳過遷移應用"
    fi
else
    print_info "如需應用遷移，請執行："
    print_info "  alembic upgrade head"
    print_info "或使用："
    print_info "  python scripts/alembic_helper.py migrate"
fi

# 8. 完成
print_header "完成"

print_success "遷移創建流程完成"
print_info "遷移檔案: $MIGRATION_FILE"

if [ -f "$BACKUP_FILE" ]; then
    print_info "備份檔案: $BACKUP_FILE"
fi

echo ""
print_info "後續步驟："
print_info "  1. 檢查遷移檔案內容: cat $MIGRATION_FILE"
print_info "  2. 驗證 upgrade() 和 downgrade() 函數"
print_info "  3. 應用遷移: alembic upgrade head"
print_info "  4. 驗證結果: alembic current"

echo ""
