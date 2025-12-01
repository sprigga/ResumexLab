"""
Resume data import service
Author: Polo (林鴻全)
Date: 2025-12-01
Purpose: 提供完整的履歷資料導入功能，包含專案資料
"""

from datetime import date
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectDetail


def import_projects_for_work_experience(db: Session, work1_id: int, work2_id: int, work3_id: int):
    """
    導入所有專案經驗
    參數:
        db: 資料庫 session
        work1_id: 鴻海科技集團的工作經歷 ID
        work2_id: 啟碁科技的工作經歷 ID
        work3_id: 台揚科技的工作經歷 ID
    返回:
        (project_count, detail_count): 專案數量和細節數量
    """

    # 鴻海科技集團的專案資料
    hon_hai_projects = [
        {
            "title_zh": "失量信號產生器及無線射頻補償功能開發",
            "title_en": "Vector Signal Generator and RF Compensation Development",
            "description_zh": "開發 SMCV100B 儀器控制程式及無線射頻補償工具，提升測試流程的自動化與精確度，優化無線通訊測試效率。",
            "description_en": "Developed SMCV100B instrument control program and RF compensation tool, enhancing test automation and accuracy, optimizing wireless communication test efficiency.",
            "technologies": "Python",
            "tools": "Visual Studio Code",
            "environment": "Windows 10",
            "start_date": date(2024, 10, 1),
            "end_date": date(2025, 3, 31),
            "details_zh": [
                "透過儀器控制程式減少人工操作，實現測試自動化，提高測試效率與一致性。",
                "透過補償機制提升數值計算精度，確保測試結果的穩定性與可靠性。"
            ],
            "details_en": [
                "Reduced manual operations through instrument control programs, achieving test automation and improving efficiency and consistency.",
                "Enhanced numerical calculation accuracy through compensation mechanisms, ensuring stability and reliability of test results."
            ]
        },
        {
            "title_zh": "EV 車載測試系統 – VW Interface Board",
            "title_en": "EV Vehicle Testing System - VW Interface Board",
            "description_zh": "開發 EV 車載系統的 FCT（功能測試）與 EOL（終端測試）軟體，提升測試效率與準確性。",
            "description_en": "Developed FCT (Functional Test) and EOL (End of Line) software for EV vehicle systems, improving test efficiency and accuracy.",
            "technologies": "Python",
            "tools": "Visual Studio Code",
            "environment": "Windows 10",
            "start_date": date(2024, 6, 1),
            "end_date": date(2024, 9, 30),
            "details_zh": [
                "架設並優化測試執行環境，提高測試穩定性。",
                "透過測試腳本及指令優化，成功縮短測試軟體執行時間。",
                "進行失效分析，提升系統可靠度並降低故障率。"
            ],
            "details_en": [
                "Set up and optimized test execution environment, improving test stability.",
                "Successfully reduced test software execution time through test script and command optimization.",
                "Conducted failure analysis, improving system reliability and reducing failure rate."
            ]
        },
        {
            "title_zh": "自動化產線 – Baseline Modbus 通訊開發",
            "title_en": "Automated Production Line - Baseline Modbus Communication Development",
            "description_zh": "開發 Modbus 通訊協議，實現產線 PLC 自動化測試，提升生產效能。",
            "description_en": "Developed Modbus communication protocol, implementing production line PLC automated testing, enhancing production efficiency.",
            "technologies": "Python",
            "tools": "Visual Studio Code",
            "environment": "Windows 10",
            "start_date": date(2024, 3, 1),
            "end_date": date(2024, 9, 30),
            "details_zh": [
                "設計並實作 PLC 交互機制，使測試流程全自動化。",
                "透過即時數據處理，提高測試精確度與產線效率。"
            ],
            "details_en": [
                "Designed and implemented PLC interaction mechanism, making test process fully automated.",
                "Improved test accuracy and production line efficiency through real-time data processing."
            ]
        },
        {
            "title_zh": "3D Printer 軟體開發",
            "title_en": "3D Printer Software Development",
            "description_zh": "負責 3D 列印機的功能設計、列印格式開發及影像錯位校正功能，提升列印精度與操作體驗。",
            "description_en": "Responsible for 3D printer function design, print format development, and image misalignment correction, improving printing accuracy and user experience.",
            "technologies": "C++, Python",
            "tools": "Qt, Visual Studio Code",
            "environment": "Windows 10, Linux Ubuntu",
            "start_date": date(2023, 3, 1),
            "end_date": date(2024, 2, 29),
            "details_zh": [
                "設計 JSON 格式取代傳統 PCL 指令，提高資料處理靈活性。",
                "實作噴嘴補償與影像編輯演算法，提升列印品質。"
            ],
            "details_en": [
                "Designed JSON format to replace traditional PCL commands, improving data processing flexibility.",
                "Implemented nozzle compensation and image editing algorithms, enhancing print quality."
            ]
        },
        {
            "title_zh": "醫療設備 – 霧化吸入器控制韌體",
            "title_en": "Medical Device - Nebulizer Control Firmware",
            "description_zh": "開發符合 ISO 13485 標準的霧化吸入器控制韌體，確保醫療器材符合國際法規。",
            "description_en": "Developed nebulizer control firmware compliant with ISO 13485 standards, ensuring medical devices meet international regulations.",
            "technologies": "C",
            "tools": "MPLAB",
            "environment": "Windows 10, Linux Ubuntu",
            "start_date": date(2022, 3, 1),
            "end_date": date(2023, 2, 28),
            "details_zh": [],
            "details_en": []
        },
        {
            "title_zh": "智慧穿戴裝置 – 智慧鞋墊",
            "title_en": "Smart Wearable Device - Smart Insole",
            "description_zh": "開發六軸感測器與藍牙數據傳輸韌體，並開發 PC 端數據接收與分析工具。",
            "description_en": "Developed six-axis sensor and Bluetooth data transmission firmware, and developed PC-side data reception and analysis tools.",
            "technologies": "C, Python",
            "tools": "Anaconda, Visual Studio Code, MPLAB",
            "environment": "Windows 10, Linux Ubuntu",
            "start_date": date(2019, 9, 1),
            "end_date": date(2022, 2, 28),
            "details_zh": [],
            "details_en": []
        },
        {
            "title_zh": "光機電掃描系統失效分析與 IoT 平台開發",
            "title_en": "Opto-Mechatronic Scanning System Failure Analysis and IoT Platform Development",
            "description_zh": "透過振動訊號分析，開發 IoT 故障預測系統，提升設備維護效率。",
            "description_en": "Developed IoT fault prediction system through vibration signal analysis, improving equipment maintenance efficiency.",
            "technologies": "Python",
            "tools": "Pandas, Anaconda, Visual Studio Code",
            "environment": "Windows, Linux Ubuntu",
            "start_date": date(2018, 8, 1),
            "end_date": date(2019, 7, 31),
            "details_zh": [
                "使用 Python 進行數據預處理與異常檢測。",
                "設計機器學習演算法，強化設備健康監測能力。"
            ],
            "details_en": [
                "Used Python for data preprocessing and anomaly detection.",
                "Designed machine learning algorithms to enhance equipment health monitoring capabilities."
            ]
        },
        {
            "title_zh": "印表機測試軟體 – UI 紙匣整合量測",
            "title_en": "Printer Testing Software - UI Paper Tray Integration Measurement",
            "description_zh": "開發 Sharp 多功能印表機測試系統，提高測試效率與準確性。",
            "description_en": "Developed Sharp multifunction printer testing system, improving test efficiency and accuracy.",
            "technologies": "C++",
            "tools": "Visual Studio",
            "environment": "Windows",
            "start_date": date(2018, 5, 1),
            "end_date": date(2018, 8, 31),
            "details_zh": [
                "設計 UI 介面，實現 A4/A3 紙張切換與測試自動化。",
                "優化測試流程，減少人工操作並縮短測試時間。"
            ],
            "details_en": [
                "Designed UI interface, achieving A4/A3 paper switching and test automation.",
                "Optimized test process, reducing manual operations and shortening test time."
            ]
        },
        {
            "title_zh": "印表機韌體測試支援 – Neo Printer",
            "title_en": "Printer Firmware Testing Support - Neo Printer",
            "description_zh": "負責 MFP（多功能印表機）測試程式開發與 UI SIM 訊息碼撰寫。",
            "description_en": "Responsible for MFP (Multi-Function Printer) test program development and UI SIM message code writing.",
            "technologies": "C++",
            "tools": "Visual Studio",
            "environment": "Windows",
            "start_date": date(2017, 12, 1),
            "end_date": date(2018, 4, 30),
            "details_zh": [],
            "details_en": []
        }
    ]

    # 啟碁科技的專案
    wistron_projects = [
        {
            "title_zh": "企業財務報表系統",
            "title_en": "Enterprise Financial Reporting System",
            "description_zh": "開發企業預算管理與 PR 單勾稽系統，提升財務流程透明度與準確性。",
            "description_en": "Developed enterprise budget management and PR reconciliation system, improving financial process transparency and accuracy.",
            "technologies": "C#.NET, SQL",
            "tools": "Visual Studio, SQL Server, Oracle Database",
            "environment": "Windows Server"
        },
        {
            "title_zh": "HR 出勤與加班預警系統",
            "title_en": "HR Attendance and Overtime Warning System",
            "description_zh": "設計自動化通知系統，確保符合勞基法規範，並提供預警報表。",
            "description_en": "Designed automated notification system, ensuring compliance with labor laws and providing warning reports.",
            "technologies": "C#.NET, SQL",
            "tools": "Visual Studio, SQL Server, Oracle Database",
            "environment": "Windows Server"
        },
        {
            "title_zh": "PLM 合約表單整合",
            "title_en": "PLM Contract Form Integration",
            "description_zh": "建立 PLM 系統與合約表單數據交換機制，提高品保部門審核效率。",
            "description_en": "Established data exchange mechanism between PLM system and contract forms, improving quality assurance department review efficiency.",
            "technologies": "C#.NET, SQL",
            "tools": "Visual Studio, SQL Server, Oracle Database",
            "environment": "Windows Server"
        },
        {
            "title_zh": "門禁與膳食系統升級",
            "title_en": "Access Control and Meal System Upgrade",
            "description_zh": "主導舊系統遷移，確保新系統平穩運行，提升企業資安與管理效能。",
            "description_en": "Led legacy system migration, ensuring smooth operation of new system, enhancing enterprise security and management efficiency.",
            "technologies": "C#.NET, SQL",
            "tools": "Visual Studio, SQL Server, Oracle Database",
            "environment": "Windows Server"
        },
        {
            "title_zh": "CSR 問卷系統",
            "title_en": "CSR Survey System",
            "description_zh": "開發企業社會責任（CSR）調查與數據分析平台，提供決策參考依據。",
            "description_en": "Developed Corporate Social Responsibility (CSR) survey and data analysis platform, providing decision-making reference.",
            "technologies": "C#.NET, SQL",
            "tools": "Visual Studio, SQL Server, Oracle Database",
            "environment": "Windows Server"
        }
    ]

    # 台揚科技的專案
    taiyen_project = {
        "title_zh": "電子表單系統導入",
        "title_en": "Electronic Form System Implementation",
        "description_zh": "將舊有 Lotus Notes 電子表單系統升級，強化流程管理與數據分析功能。",
        "description_en": "Upgraded legacy Lotus Notes electronic form system, enhancing process management and data analysis functions.",
        "technologies": "JavaScript, jQuery, C#.NET, SQL",
        "tools": "SQL Server, Oracle Database",
        "environment": "Windows Server"
    }

    project_count = 0
    detail_count = 0

    # 導入鴻海專案
    for i, proj_data in enumerate(hon_hai_projects, 1):
        project = Project(
            work_experience_id=work1_id,
            title_zh=proj_data["title_zh"],
            title_en=proj_data["title_en"],
            description_zh=proj_data["description_zh"],
            description_en=proj_data["description_en"],
            technologies=proj_data["technologies"],
            tools=proj_data["tools"],
            environment=proj_data["environment"],
            start_date=proj_data["start_date"],
            end_date=proj_data["end_date"],
            display_order=i
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_count += 1

        # 添加專案細節
        for j, detail_zh in enumerate(proj_data["details_zh"], 1):
            detail = ProjectDetail(
                project_id=project.id,
                description_zh=detail_zh,
                description_en=proj_data["details_en"][j-1] if j-1 < len(proj_data["details_en"]) else "",
                display_order=j
            )
            db.add(detail)
            detail_count += 1
        db.commit()

    # 導入啟碁專案
    for i, proj_data in enumerate(wistron_projects, 1):
        project = Project(
            work_experience_id=work2_id,
            title_zh=proj_data["title_zh"],
            title_en=proj_data["title_en"],
            description_zh=proj_data["description_zh"],
            description_en=proj_data["description_en"],
            technologies=proj_data["technologies"],
            tools=proj_data["tools"],
            environment=proj_data["environment"],
            display_order=i
        )
        db.add(project)
        project_count += 1
    db.commit()

    # 導入台揚專案
    project = Project(
        work_experience_id=work3_id,
        title_zh=taiyen_project["title_zh"],
        title_en=taiyen_project["title_en"],
        description_zh=taiyen_project["description_zh"],
        description_en=taiyen_project["description_en"],
        technologies=taiyen_project["technologies"],
        tools=taiyen_project["tools"],
        environment=taiyen_project["environment"],
        display_order=1
    )
    db.add(project)
    db.commit()
    project_count += 1

    return project_count, detail_count
