#!/bin/bash
# Alembic 問題診斷腳本
#
# 此腳本用於快速診斷 Alembic 遷移問題
# 包含自動檢測和修復常見問題的功能
#
# 使用方法：
#   ./alembic_diagnose.sh
#
# 作者: Polo (林鴻全)
# 日期: 2026-01-04

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
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

print_fix() {
    echo -e "${GREEN}${BOLD}🔧 修復方案: $1${NC}"
}

# 取得腳本所在目錄
# 原本路徑邏輯 (已註解於 2026-01-04，原因：腳本移動到 backend/scripts/)
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# BACKEND_DIR="$PROJECT_ROOT/backend"

# 新路徑邏輯 (修改於 2026-01-04，原因：腳本現在位於 backend/scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # backend/scripts/
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"                          # backend/
PROJECT_ROOT="$(dirname "$BACKEND_DIR")"                        # project root

# 問題計數器
ISSUES_FOUND=0
FIXES_SUGGESTED=0

print_header "Alembic 問題診斷工具"

# 切換到 backend 目錄
if [ ! -d "$BACKEND_DIR" ]; then
    print_error "找不到 backend 目錄: $BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR"
print_info "工作目錄: $BACKEND_DIR"

# ========================================
# 檢查 1: 虛擬環境
# ========================================
print_header "檢查 1: 虛擬環境"

if [ -d ".venv" ]; then
    print_success "虛擬環境存在"

    # 檢查 alembic 是否安裝
    if [ -f ".venv/bin/alembic" ]; then
        print_success "Alembic 已安裝"

        # 取得版本
        source .venv/bin/activate
        ALEMBIC_VERSION=$(alembic --version 2>&1 | grep -v "^INFO")
        print_info "版本: $ALEMBIC_VERSION"
    else
        print_error "Alembic 未安裝"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
        print_fix "執行: pip install alembic"
        FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
    fi
else
    print_error "虛擬環境不存在"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    print_fix "執行: python -m venv .venv"
    FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
    exit 1
fi

# ========================================
# 檢查 2: Alembic 配置
# ========================================
print_header "檢查 2: Alembic 配置"

if [ -f "alembic.ini" ]; then
    print_success "alembic.ini 存在"

    # 檢查資料庫 URL 設定
    DB_URL=$(grep "^sqlalchemy.url" alembic.ini | cut -d'=' -f2 | xargs)
    if [ ! -z "$DB_URL" ]; then
        print_success "資料庫 URL 已設定"
        print_info "URL: $DB_URL"
    else
        print_warning "資料庫 URL 未設定"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    print_error "alembic.ini 不存在"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    print_fix "執行: alembic init alembic"
    FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
    exit 1
fi

if [ -d "alembic" ]; then
    print_success "alembic 目錄存在"

    # 檢查 env.py
    if [ -f "alembic/env.py" ]; then
        print_success "env.py 存在"

        # 檢查 target_metadata 設定
        if grep -q "target_metadata = Base.metadata" alembic/env.py; then
            print_success "target_metadata 已設定"
        else
            print_warning "target_metadata 可能未正確設定"
            print_info "請確認 alembic/env.py 中有: target_metadata = Base.metadata"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        fi
    else
        print_error "env.py 不存在"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # 檢查 versions 目錄
    if [ -d "alembic/versions" ]; then
        MIGRATION_COUNT=$(ls -1 alembic/versions/*.py 2>/dev/null | wc -l)
        print_success "versions 目錄存在 ($MIGRATION_COUNT 個遷移)"
    else
        print_error "versions 目錄不存在"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    print_error "alembic 目錄不存在"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    exit 1
fi

# ========================================
# 檢查 3: 資料庫狀態
# ========================================
print_header "檢查 3: 資料庫狀態"

if [ -f "data/resume.db" ]; then
    DB_SIZE=$(du -h data/resume.db | cut -f1)
    print_success "資料庫存在 (大小: $DB_SIZE)"

    # 使用 sqlite3 檢查表
    if command -v sqlite3 &> /dev/null; then
        # 檢查 alembic_version 表
        if sqlite3 data/resume.db "SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version';" | grep -q "alembic_version"; then
            print_success "alembic_version 表存在"

            # 取得當前版本
            CURRENT_VERSION=$(sqlite3 data/resume.db "SELECT version_num FROM alembic_version;" 2>/dev/null)
            if [ ! -z "$CURRENT_VERSION" ]; then
                print_success "資料庫已標記版本: $CURRENT_VERSION"
            else
                print_warning "資料庫未標記版本"
                print_info "可能原因: 首次設定或資料庫未初始化"
                ISSUES_FOUND=$((ISSUES_FOUND + 1))
                print_fix "執行: alembic stamp head"
                FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
            fi
        else
            print_warning "alembic_version 表不存在"
            print_info "這是正常的，如果這是首次使用 Alembic"
        fi

        # 列出所有表
        TABLE_COUNT=$(sqlite3 data/resume.db "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';" 2>/dev/null)
        print_info "資料庫中有 $TABLE_COUNT 個表"

        if [ $TABLE_COUNT -gt 0 ]; then
            print_info "表列表:"
            sqlite3 data/resume.db "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;" | while read table; do
                echo "  - $table"
            done
        fi
    else
        print_warning "未安裝 sqlite3 指令，無法檢查資料庫內容"
    fi
else
    print_warning "資料庫不存在"
    print_info "這是正常的，如果尚未執行首次遷移"
fi

# ========================================
# 檢查 4: 遷移一致性
# ========================================
print_header "檢查 4: 遷移一致性"

# 取得 Alembic 當前版本
ALEMBIC_CURRENT=$(alembic current 2>&1 | grep -v "^INFO" | head -1 | awk '{print $1}')
ALEMBIC_HEAD=$(alembic heads 2>&1 | grep -v "^INFO" | head -1 | awk '{print $1}')

if [ ! -z "$ALEMBIC_HEAD" ]; then
    print_success "Alembic HEAD: $ALEMBIC_HEAD"
else
    print_warning "無法取得 Alembic HEAD"
fi

if [ ! -z "$ALEMBIC_CURRENT" ]; then
    print_success "當前版本: $ALEMBIC_CURRENT"

    if [ "$ALEMBIC_CURRENT" == "$ALEMBIC_HEAD" ]; then
        print_success "資料庫是最新版本"
    else
        print_warning "資料庫不是最新版本"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
        print_fix "執行: alembic upgrade head"
        FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
    fi
else
    print_warning "資料庫尚未標記版本"

    if [ -f "data/resume.db" ]; then
        # 檢查是否有表存在
        if [ $TABLE_COUNT -gt 1 ]; then
            print_warning "資料庫有表但未標記版本"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
            print_fix "執行: alembic stamp head"
            FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
        fi
    fi
fi

# ========================================
# 檢查 5: SQLite 兼容性問題
# ========================================
print_header "檢查 5: SQLite 兼容性"

# 檢查最新遷移檔案
LATEST_MIGRATION=$(ls -t alembic/versions/*.py 2>/dev/null | head -1)

if [ ! -z "$LATEST_MIGRATION" ]; then
    print_info "檢查最新遷移: $(basename $LATEST_MIGRATION)"

    if grep -q "op.alter_column" "$LATEST_MIGRATION"; then
        print_error "發現 SQLite 不支援的 ALTER COLUMN 操作"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))

        ALTER_COUNT=$(grep -c "op.alter_column" "$LATEST_MIGRATION")
        print_warning "找到 $ALTER_COUNT 個 alter_column 操作"

        print_fix "執行: python $SCRIPT_DIR/alembic_helper.py fix-sqlite"
        FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
    else
        print_success "未發現 SQLite 兼容性問題"
    fi
else
    print_warning "找不到遷移檔案"
fi

# ========================================
# 檢查 6: 常見錯誤
# ========================================
print_header "檢查 6: 常見錯誤診斷"

# 嘗試執行 alembic check
print_info "執行: alembic check"
CHECK_OUTPUT=$(alembic check 2>&1)
CHECK_STATUS=$?

if [ $CHECK_STATUS -eq 0 ]; then
    print_success "Alembic 檢查通過"
else
    print_warning "Alembic 檢查發現問題"
    echo "$CHECK_OUTPUT"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

# 檢查 Python cache
if [ -d "app/__pycache__" ] || [ -d "alembic/__pycache__" ]; then
    print_warning "發現 Python cache 目錄"
    print_info "建議清除 cache 以避免潛在問題"
    print_fix "執行: find . -type d -name __pycache__ -exec rm -r {} +"
    FIXES_SUGGESTED=$((FIXES_SUGGESTED + 1))
fi

# ========================================
# 總結
# ========================================
print_header "診斷總結"

if [ $ISSUES_FOUND -eq 0 ]; then
    print_success "未發現問題！系統狀態良好"
else
    print_warning "發現 $ISSUES_FOUND 個問題"

    if [ $FIXES_SUGGESTED -gt 0 ]; then
        echo ""
        print_info "建議執行以下修復操作："
        print_info "  1. 查看上方標記的 🔧 修復方案"
        print_info "  2. 依序執行建議的指令"
        print_info "  3. 再次執行本診斷腳本驗證"
    fi
fi

echo ""
print_info "如需更多協助，請參考:"
print_info "  - 文件: docs/Alembic.md"
print_info "  - 助手: python $SCRIPT_DIR/alembic_helper.py help"

echo ""
