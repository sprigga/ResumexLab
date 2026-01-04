#!/usr/bin/env python3
"""
Alembic 遷移助手腳本

功能：
1. 檢查 Alembic 狀態
2. 自動修復常見問題
3. 備份資料庫
4. 執行遷移
5. 驗證遷移結果

使用方法：
    python alembic_helper.py [command]

Commands:
    status      - 檢查當前 Alembic 狀態
    check       - 執行健康檢查
    backup      - 備份資料庫
    migrate     - 執行遷移（會自動備份）
    stamp       - 標記資料庫版本
    fix-sqlite  - 修復 SQLite ALTER COLUMN 問題
    rollback    - 回滾到上一個版本

作者: Polo (林鴻全)
日期: 2026-01-04
"""

import os
import sys
import subprocess
import shutil
import re
from datetime import datetime
from pathlib import Path


class Colors:
    """終端機顏色輸出"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AlembicHelper:
    def __init__(self):
        # 檢測工作目錄
        # 原本路徑邏輯 (已註解於 2026-01-04，原因：腳本移動到 backend/scripts/)
        # self.script_dir = Path(__file__).parent.absolute()
        # self.project_root = self.script_dir.parent
        # self.backend_dir = self.project_root / "backend"

        # 新路徑邏輯 (修改於 2026-01-04，原因：腳本現在位於 backend/scripts/)
        self.script_dir = Path(__file__).parent.absolute()  # backend/scripts/
        self.backend_dir = self.script_dir.parent           # backend/
        self.project_root = self.backend_dir.parent         # project root

        # 確認是否在正確的目錄
        if not self.backend_dir.exists():
            self.error("找不到 backend 目錄")
            sys.exit(1)

        # 資料庫路徑
        self.db_path = self.backend_dir / "data" / "resume.db"
        self.backup_dir = self.backend_dir / "data"
        self.alembic_dir = self.backend_dir / "alembic"
        self.versions_dir = self.alembic_dir / "versions"

    def print_header(self, text):
        """列印標題"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

    def success(self, text):
        """成功訊息"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

    def warning(self, text):
        """警告訊息"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

    def error(self, text):
        """錯誤訊息"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def info(self, text):
        """資訊訊息"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

    def run_alembic_command(self, args, capture_output=True):
        """執行 Alembic 指令"""
        try:
            # 切換到 backend 目錄
            os.chdir(self.backend_dir)

            # 啟動虛擬環境並執行指令
            cmd = f"source .venv/bin/activate && alembic {args}"

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                executable="/bin/bash"
            )

            return result
        except Exception as e:
            self.error(f"執行 Alembic 指令失敗: {e}")
            return None

    def check_status(self):
        """檢查 Alembic 狀態"""
        self.print_header("檢查 Alembic 狀態")

        # 1. 檢查資料庫是否存在
        if self.db_path.exists():
            self.success(f"資料庫存在: {self.db_path}")
            size = self.db_path.stat().st_size / 1024  # KB
            self.info(f"資料庫大小: {size:.2f} KB")
        else:
            self.warning(f"資料庫不存在: {self.db_path}")

        # 2. 檢查當前版本
        self.info("查詢當前資料庫版本...")
        result = self.run_alembic_command("current")
        if result and result.returncode == 0:
            output = result.stdout.strip()
            if output and "INFO" in output:
                # 提取版本號
                lines = output.split('\n')
                version_line = [line for line in lines if not line.startswith('INFO')]
                if version_line:
                    self.success(f"當前版本: {version_line[0]}")
                else:
                    self.warning("資料庫尚未標記版本")
            else:
                self.warning("資料庫尚未標記版本")

        # 3. 檢查遷移歷史
        self.info("查詢遷移歷史...")
        result = self.run_alembic_command("history")
        if result and result.returncode == 0:
            # 計算遷移檔案數量
            migration_count = len(list(self.versions_dir.glob("*.py")))
            self.success(f"找到 {migration_count} 個遷移檔案")

        # 4. 檢查是否有待套用的遷移
        self.info("檢查待套用的遷移...")
        result = self.run_alembic_command("heads")
        if result and result.returncode == 0:
            self.info("最新版本: " + result.stdout.strip().split('\n')[-1])

    def backup_database(self):
        """備份資料庫"""
        self.print_header("備份資料庫")

        if not self.db_path.exists():
            self.warning("資料庫不存在，無需備份")
            return None

        # 生成備份檔名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"resume_backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_name

        try:
            shutil.copy2(self.db_path, backup_path)
            self.success(f"備份完成: {backup_path}")

            # 顯示備份大小
            size = backup_path.stat().st_size / 1024  # KB
            self.info(f"備份大小: {size:.2f} KB")

            return backup_path
        except Exception as e:
            self.error(f"備份失敗: {e}")
            return None

    def stamp_head(self):
        """標記資料庫為最新版本"""
        self.print_header("標記資料庫版本")

        self.warning("此操作會將資料庫標記為最新版本（不執行遷移）")
        confirm = input("確定要繼續嗎? (y/N): ")

        if confirm.lower() != 'y':
            self.info("操作已取消")
            return

        result = self.run_alembic_command("stamp head", capture_output=False)

        if result and result.returncode == 0:
            self.success("版本標記完成")
            # 顯示當前版本
            self.run_alembic_command("current", capture_output=False)
        else:
            self.error("版本標記失敗")

    def migrate(self):
        """執行遷移"""
        self.print_header("執行資料庫遷移")

        # 1. 先備份
        self.info("執行遷移前會自動備份資料庫...")
        backup_path = self.backup_database()

        if not backup_path:
            self.warning("備份失敗，但可以繼續執行遷移")
            confirm = input("確定要繼續嗎? (y/N): ")
            if confirm.lower() != 'y':
                self.info("操作已取消")
                return

        # 2. 執行遷移
        self.info("開始執行遷移...")
        result = self.run_alembic_command("upgrade head", capture_output=False)

        if result and result.returncode == 0:
            self.success("遷移執行成功")

            # 3. 顯示當前版本
            print()
            self.info("當前版本:")
            self.run_alembic_command("current", capture_output=False)
        else:
            self.error("遷移執行失敗")
            if backup_path:
                self.info(f"如需恢復，請使用備份: {backup_path}")

    def fix_sqlite_alter_column(self):
        """修復 SQLite ALTER COLUMN 問題"""
        self.print_header("修復 SQLite ALTER COLUMN 問題")

        self.info("掃描最新的遷移檔案...")

        # 找出最新的遷移檔案
        migration_files = sorted(self.versions_dir.glob("*.py"), key=os.path.getmtime, reverse=True)

        if not migration_files:
            self.warning("找不到遷移檔案")
            return

        latest_migration = migration_files[0]
        self.info(f"最新遷移檔案: {latest_migration.name}")

        # 讀取檔案內容
        with open(latest_migration, 'r', encoding='utf-8') as f:
            content = f.read()

        # 檢查是否包含 alter_column
        if 'op.alter_column' not in content:
            self.success("此遷移檔案不包含 alter_column 操作，無需修復")
            return

        self.warning("發現 alter_column 操作！")
        print(f"\n{Colors.WARNING}包含以下 alter_column 操作:{Colors.ENDC}")

        # 找出所有 alter_column 行
        lines = content.split('\n')
        alter_lines = []
        for i, line in enumerate(lines, 1):
            if 'op.alter_column' in line:
                alter_lines.append((i, line))
                print(f"  行 {i}: {line.strip()}")

        print()
        self.warning("SQLite 不支援 ALTER COLUMN 操作")
        self.info("建議: 手動編輯檔案，將 alter_column 相關行註解掉")

        confirm = input("\n是否自動註解這些行? (y/N): ")

        if confirm.lower() != 'y':
            self.info("操作已取消")
            self.info(f"請手動編輯: {latest_migration}")
            return

        # 自動註解
        self.info("正在自動註解 alter_column 操作...")

        # 添加註解說明
        comment_header = f"    # 原本的 ALTER COLUMN 操作 (已註解於 {datetime.now().strftime('%Y-%m-%d')}，原因：SQLite 不支援 ALTER COLUMN)\n"

        # 處理 upgrade 和 downgrade 函數
        new_lines = []
        in_alter_block = False
        indent = ""

        for i, line in enumerate(lines):
            if 'op.alter_column' in line:
                if not in_alter_block:
                    # 第一次遇到，添加註解說明
                    indent = line[:len(line) - len(line.lstrip())]
                    new_lines.append(comment_header)
                    in_alter_block = True
                new_lines.append(indent + "# " + line.strip())
            elif in_alter_block:
                # 檢查是否還在同一個區塊（縮排相同或更多）
                current_indent = line[:len(line) - len(line.lstrip())]
                if line.strip() and len(current_indent) <= len(indent) and not line.strip().startswith(')'):
                    in_alter_block = False
                    new_lines.append(line)
                else:
                    new_lines.append(indent + "# " + line.strip())
            else:
                new_lines.append(line)

        # 備份原檔案
        backup_path = latest_migration.with_suffix('.py.bak')
        shutil.copy2(latest_migration, backup_path)
        self.success(f"原檔案已備份: {backup_path}")

        # 寫入修改後的內容
        with open(latest_migration, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        self.success("修復完成！")
        self.info("現在可以執行 'python alembic_helper.py migrate' 來套用遷移")

    def rollback(self):
        """回滾到上一個版本"""
        self.print_header("回滾資料庫遷移")

        self.warning("此操作會將資料庫回滾到上一個版本")

        # 先備份
        self.info("執行回滾前會自動備份資料庫...")
        backup_path = self.backup_database()

        confirm = input("確定要回滾嗎? (y/N): ")

        if confirm.lower() != 'y':
            self.info("操作已取消")
            return

        result = self.run_alembic_command("downgrade -1", capture_output=False)

        if result and result.returncode == 0:
            self.success("回滾完成")
            # 顯示當前版本
            print()
            self.info("當前版本:")
            self.run_alembic_command("current", capture_output=False)
        else:
            self.error("回滾失敗")
            if backup_path:
                self.info(f"備份位於: {backup_path}")

    def health_check(self):
        """健康檢查"""
        self.print_header("Alembic 健康檢查")

        checks = []

        # 1. 檢查 backend 目錄
        if self.backend_dir.exists():
            checks.append(("Backend 目錄", True, str(self.backend_dir)))
        else:
            checks.append(("Backend 目錄", False, "目錄不存在"))

        # 2. 檢查虛擬環境
        venv_path = self.backend_dir / ".venv"
        if venv_path.exists():
            checks.append(("虛擬環境", True, str(venv_path)))
        else:
            checks.append(("虛擬環境", False, "虛擬環境不存在"))

        # 3. 檢查 alembic.ini
        alembic_ini = self.backend_dir / "alembic.ini"
        if alembic_ini.exists():
            checks.append(("Alembic 配置", True, str(alembic_ini)))
        else:
            checks.append(("Alembic 配置", False, "alembic.ini 不存在"))

        # 4. 檢查遷移目錄
        if self.versions_dir.exists():
            migration_count = len(list(self.versions_dir.glob("*.py")))
            checks.append(("遷移目錄", True, f"{migration_count} 個遷移檔案"))
        else:
            checks.append(("遷移目錄", False, "versions 目錄不存在"))

        # 5. 檢查資料庫
        if self.db_path.exists():
            size = self.db_path.stat().st_size / 1024
            checks.append(("資料庫檔案", True, f"{size:.2f} KB"))
        else:
            checks.append(("資料庫檔案", False, "資料庫不存在"))

        # 6. 檢查 Alembic 是否可用
        result = self.run_alembic_command("--help")
        if result and result.returncode == 0:
            checks.append(("Alembic 指令", True, "可正常執行"))
        else:
            checks.append(("Alembic 指令", False, "無法執行 alembic 指令"))

        # 輸出檢查結果
        print(f"\n{'項目':<20} {'狀態':<10} {'詳情':<40}")
        print("-" * 70)

        all_passed = True
        for name, passed, detail in checks:
            status = f"{Colors.OKGREEN}✓ 通過{Colors.ENDC}" if passed else f"{Colors.FAIL}✗ 失敗{Colors.ENDC}"
            print(f"{name:<20} {status:<20} {detail:<40}")
            if not passed:
                all_passed = False

        print()
        if all_passed:
            self.success("所有檢查通過！")
        else:
            self.warning("部分檢查失敗，請檢查環境配置")

    def show_help(self):
        """顯示幫助訊息"""
        self.print_header("Alembic Helper - 使用說明")

        print(f"{Colors.BOLD}可用指令:{Colors.ENDC}\n")

        commands = [
            ("status", "檢查當前 Alembic 狀態"),
            ("check", "執行健康檢查"),
            ("backup", "備份資料庫"),
            ("migrate", "執行遷移（會自動備份）"),
            ("stamp", "標記資料庫版本"),
            ("fix-sqlite", "修復 SQLite ALTER COLUMN 問題"),
            ("rollback", "回滾到上一個版本"),
            ("help", "顯示此幫助訊息"),
        ]

        for cmd, desc in commands:
            print(f"  {Colors.OKCYAN}{cmd:<15}{Colors.ENDC} {desc}")

        print(f"\n{Colors.BOLD}使用範例:{Colors.ENDC}\n")
        print(f"  python alembic_helper.py status")
        print(f"  python alembic_helper.py migrate")
        print(f"  python alembic_helper.py fix-sqlite")
        print()


def main():
    helper = AlembicHelper()

    if len(sys.argv) < 2:
        helper.show_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    commands = {
        'status': helper.check_status,
        'check': helper.health_check,
        'backup': helper.backup_database,
        'migrate': helper.migrate,
        'stamp': helper.stamp_head,
        'fix-sqlite': helper.fix_sqlite_alter_column,
        'rollback': helper.rollback,
        'help': helper.show_help,
    }

    if command in commands:
        try:
            commands[command]()
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}操作已中斷{Colors.ENDC}")
            sys.exit(1)
        except Exception as e:
            helper.error(f"執行失敗: {e}")
            sys.exit(1)
    else:
        helper.error(f"未知指令: {command}")
        helper.show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
