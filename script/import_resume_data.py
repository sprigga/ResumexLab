"""
Script to import resume data from PDF to database
Author: Polo (林鴻全)
Date: 2025-11-29
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# 確保在正確的目錄下執行，這樣相對路徑的資料庫才能被找到
backend_dir = Path(__file__).parent.parent / "backend"
os.chdir(backend_dir)

from datetime import date
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.personal_info import PersonalInfo
from app.models.work_experience import WorkExperience
from app.models.project import Project, ProjectDetail
from app.models.education import Education
from app.models.certification import Certification, Language
from app.models.publication import Publication, GithubProject


def clear_existing_data(db: Session):
    """清除現有履歷資料（保留使用者資料）"""
    print("正在清除現有履歷資料...")
    db.query(ProjectDetail).delete()
    db.query(Project).delete()
    db.query(WorkExperience).delete()
    db.query(Education).delete()
    db.query(Certification).delete()
    db.query(Language).delete()
    db.query(Publication).delete()
    db.query(GithubProject).delete()
    db.query(PersonalInfo).delete()
    db.commit()
    print("現有資料已清除")


def import_personal_info(db: Session):
    """導入個人資訊"""
    print("\n正在導入個人資訊...")

    personal_info = PersonalInfo(
        name_zh="林鴻全",
        name_en="Hung Chuan Lin",
        phone="0926-593-172",
        email="sprigga@gmail.com",
        address_zh="台南市安南區北安路三段305巷3號4樓之1",
        address_en="4F.-1, No. 3, Ln. 305, Pei'an Rd., Annan Dist., Tainan City 709004",
        objective_zh="尋求資訊工程師或測試工程師職位，運用豐富的軟體開發經驗與系統整合能力，專注於提升系統效能與技術創新，為企業創造卓越價值。",
        objective_en="Seeking a position as an IT Customer Engineer or Test Engineer, leveraging extensive software development experience and system integration capabilities, focusing on improving system performance and technological innovation to create outstanding value for enterprises.",
        personality_zh="做事情有毅力，樂觀開朗，好與人分享心得，並且善於發現潛在問題並提前解決。",
        personality_en="Persistent in work, optimistic and cheerful, enjoys sharing insights with others, and skilled at discovering potential problems and solving them proactively.",
        summary_zh="""擁有十多年資訊工程與軟體開發經驗，專精於系統設計、測試開發及技術整合，熟悉 C#、Python 等主流程式語言，並具備 IoT、醫療設備與自動化測試開發經驗。

曾負責多個關鍵專案，包括印表機控制、醫療設備韌體開發、EV 車載測試系統與 AI 影像處理，並成功優化系統效能、縮短測試流程，提高產品穩定性。擅長需求分析、問題排除與跨部門協作，能夠快速學習並適應新技術，致力於提升工作效率與產品品質。

熱衷於技術創新與持續學習，擁有高度責任感與團隊合作精神，善於發現問題並提供有效解決方案，期望能為企業帶來技術突破與競爭優勢。""",
        summary_en="""Over ten years of experience in information engineering and software development, specializing in system design, test development, and technology integration. Proficient in mainstream programming languages such as C# and Python, with experience in IoT, medical device development, and automated testing.

Led multiple critical projects including printer control, medical device firmware development, EV vehicle testing systems, and AI image processing, successfully optimizing system performance, streamlining testing processes, and improving product stability. Skilled in requirement analysis, troubleshooting, and cross-departmental collaboration, capable of rapidly learning and adapting to new technologies, committed to enhancing work efficiency and product quality.

Passionate about technological innovation and continuous learning, possessing strong responsibility and team spirit, adept at identifying problems and providing effective solutions, aspiring to bring technological breakthroughs and competitive advantages to enterprises."""
    )

    db.add(personal_info)
    db.commit()
    print("✓ 個人資訊導入完成")


def import_work_experience(db: Session):
    """導入工作經歷"""
    print("\n正在導入工作經歷...")

    # 鴻海科技集團
    work1 = WorkExperience(
        company_zh="鴻海科技集團",
        company_en="Hon Hai Technology Group",
        position_zh="專案工程師",
        position_en="Project Engineer",
        location_zh="台灣新竹",
        location_en="Hsinchu, Taiwan",
        start_date=date(2017, 11, 1),
        end_date=None,
        is_current=True,
        description_zh="負責印表機、醫療設備、EV 車載系統等專案的軟體開發與系統測試，具備嵌入式系統開發、自動化測試與物聯網（IoT）應用經驗。熟稔 Python、C#，並善於系統效能優化與問題分析，確保產品穩定性與高效能運作。",
        description_en="Spearheaded software development and system testing for projects involving printers, medical equipment, and EV vehicle systems. Experienced in embedded system development, automated testing, and IoT applications. Proficient in Python and C#, skilled in system performance optimization and problem analysis, ensuring product stability and high-performance operation.",
        display_order=1
    )
    db.add(work1)
    db.commit()
    db.refresh(work1)

    # 啟碁科技
    work2 = WorkExperience(
        company_zh="啟碁科技",
        company_en="Wistron NeWeb Corporation",
        position_zh="軟體應用工程師",
        position_en="Software Application Engineer",
        location_zh="台灣新竹",
        location_en="Hsinchu, Taiwan",
        start_date=date(2014, 7, 1),
        end_date=date(2017, 9, 30),
        is_current=False,
        description_zh="專注於企業內部系統開發與維護，負責需求分析、系統設計、資料庫管理與自動化報表開發，提升企業營運效率與數據準確性。",
        description_en="Focused on enterprise internal system development and maintenance, responsible for requirement analysis, system design, database management, and automated report development, improving enterprise operational efficiency and data accuracy.",
        display_order=2
    )
    db.add(work2)
    db.commit()
    db.refresh(work2)

    # 台揚科技
    work3 = WorkExperience(
        company_zh="台揚科技",
        company_en="Taiyen Technology",
        position_zh="資訊工程師",
        position_en="IT Engineer",
        location_zh="台灣新竹",
        location_en="Hsinchu, Taiwan",
        start_date=date(2011, 5, 1),
        end_date=date(2014, 6, 30),
        is_current=False,
        description_zh="負責企業內部系統開發與 BPM（業務流程管理）系統維護，提升企業流程自動化與數據整合能力。",
        description_en="Responsible for enterprise internal system development and BPM (Business Process Management) system maintenance, enhancing enterprise process automation and data integration capabilities.",
        display_order=3
    )
    db.add(work3)
    db.commit()
    db.refresh(work3)

    # 中原大學
    work4 = WorkExperience(
        company_zh="中原大學 特殊教育學系",
        company_en="Chung Yuan Christian University - Special Education Department",
        position_zh="行政助教",
        position_en="Administrative Assistant",
        location_zh="台灣桃園",
        location_en="Taoyuan, Taiwan",
        start_date=date(2005, 7, 1),
        end_date=date(2007, 8, 31),
        is_current=False,
        description_zh="負責系所日常行政事務，包括文件處理、資料管理、會議安排與記錄等，確保教學與學習活動的順利進行。",
        description_en="Responsible for daily administrative affairs of the department, including document processing, data management, meeting arrangements and records, ensuring smooth teaching and learning activities.",
        display_order=4
    )
    db.add(work4)
    db.commit()
    db.refresh(work4)

    print(f"✓ 工作經歷導入完成 ({db.query(WorkExperience).count()} 筆)")

    return work1.id, work2.id, work3.id


def import_projects(db: Session, work1_id: int, work2_id: int, work3_id: int):
    """導入專案經驗"""
    print("\n正在導入專案經驗...")

    # 鴻海科技集團的專案
    projects_data = [
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

    project_count = 0
    for i, proj_data in enumerate(projects_data, 1):
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

        # Add project details
        # Modified on 2025-11-30: 修正欄位名稱為 description_zh 和 description_en（根據資料庫模型）
        for j, detail_zh in enumerate(proj_data["details_zh"], 1):
            detail = ProjectDetail(
                project_id=project.id,
                description_zh=detail_zh,  # 修正：原為 detail_zh，改為 description_zh
                description_en=proj_data["details_en"][j-1] if j-1 < len(proj_data["details_en"]) else "",  # 修正：原為 detail_en，改為 description_en
                display_order=j
            )
            db.add(detail)
        db.commit()

    # 啟碁科技的專案
    wistron_projects = [
        {
            "title_zh": "企業財務報表系統",
            "title_en": "Enterprise Financial Reporting System",
            "description_zh": "開發企業預算管理與 PR 單勾稽系統，提升財務流程透明度與準確性。",
            "description_en": "Developed enterprise budget management and PR reconciliation system, improving financial process transparency and accuracy."
        },
        {
            "title_zh": "HR 出勤與加班預警系統",
            "title_en": "HR Attendance and Overtime Warning System",
            "description_zh": "設計自動化通知系統，確保符合勞基法規範，並提供預警報表。",
            "description_en": "Designed automated notification system, ensuring compliance with labor laws and providing warning reports."
        },
        {
            "title_zh": "PLM 合約表單整合",
            "title_en": "PLM Contract Form Integration",
            "description_zh": "建立 PLM 系統與合約表單數據交換機制，提高品保部門審核效率。",
            "description_en": "Established data exchange mechanism between PLM system and contract forms, improving quality assurance department review efficiency."
        },
        {
            "title_zh": "門禁與膳食系統升級",
            "title_en": "Access Control and Meal System Upgrade",
            "description_zh": "主導舊系統遷移，確保新系統平穩運行，提升企業資安與管理效能。",
            "description_en": "Led legacy system migration, ensuring smooth operation of new system, enhancing enterprise security and management efficiency."
        },
        {
            "title_zh": "CSR 問卷系統",
            "title_en": "CSR Survey System",
            "description_zh": "開發企業社會責任（CSR）調查與數據分析平台，提供決策參考依據。",
            "description_en": "Developed Corporate Social Responsibility (CSR) survey and data analysis platform, providing decision-making reference."
        }
    ]

    for i, proj_data in enumerate(wistron_projects, 1):
        project = Project(
            work_experience_id=work2_id,
            title_zh=proj_data["title_zh"],
            title_en=proj_data["title_en"],
            description_zh=proj_data["description_zh"],
            description_en=proj_data["description_en"],
            technologies="C#.NET, SQL",
            tools="Visual Studio, SQL Server, Oracle Database",
            environment="Windows Server",
            display_order=i
        )
        db.add(project)
        project_count += 1
    db.commit()

    # 台揚科技的專案
    taiyen_project = Project(
        work_experience_id=work3_id,
        title_zh="電子表單系統導入",
        title_en="Electronic Form System Implementation",
        description_zh="將舊有 Lotus Notes 電子表單系統升級，強化流程管理與數據分析功能。",
        description_en="Upgraded legacy Lotus Notes electronic form system, enhancing process management and data analysis functions.",
        technologies="JavaScript, jQuery, C#.NET, SQL",
        tools="SQL Server, Oracle Database",
        environment="Windows Server",
        display_order=1
    )
    db.add(taiyen_project)
    db.commit()
    project_count += 1

    print(f"✓ 專案經驗導入完成 ({project_count} 筆)")


def import_education(db: Session):
    """導入教育背景"""
    print("\n正在導入教育背景...")

    education_data = [
        {
            "school_zh": "中原大學",
            "school_en": "Chung Yuan Christian University",
            "degree_zh": "碩士",
            "degree_en": "Master",
            "major_zh": "資訊管理所",
            "major_en": "Information Management",
            "start_date": date(2008, 9, 1),
            "end_date": date(2011, 6, 30),
            "description_zh": "專案：教育部的車載資通訊專案",
            "description_en": "Project: Ministry of Education's Vehicle Telematics Project"
        },
        {
            "school_zh": "朝陽科技大學",
            "school_en": "Chaoyang University of Technology",
            "degree_zh": "學士",
            "degree_en": "Bachelor",
            "major_zh": "資訊管理系",
            "major_en": "Information Management",
            "start_date": date(2001, 9, 1),
            "end_date": date(2003, 6, 30),
            "description_zh": "專案：網路多媒體相關",
            "description_en": "Project: Network Multimedia Related"
        }
    ]

    for i, edu_data in enumerate(education_data, 1):
        education = Education(
            school_zh=edu_data["school_zh"],
            school_en=edu_data["school_en"],
            degree_zh=edu_data["degree_zh"],
            degree_en=edu_data["degree_en"],
            major_zh=edu_data["major_zh"],
            major_en=edu_data["major_en"],
            start_date=edu_data["start_date"],
            end_date=edu_data["end_date"],
            description_zh=edu_data["description_zh"],
            description_en=edu_data["description_en"],
            display_order=i
        )
        db.add(education)

    db.commit()
    print(f"✓ 教育背景導入完成 ({db.query(Education).count()} 筆)")


def import_certifications(db: Session):
    """導入證照"""
    print("\n正在導入證照...")

    certifications_data = [
        {
            "name_zh": "CCNA",
            "name_en": "CCNA (Cisco Certified Network Associate)",
            "issuer": "Cisco",
            "issue_date": date(2007, 1, 1),
            "certificate_number": "393834169014JOBN"
        },
        {
            "name_zh": "ISMS 稽核員/主導稽核員培訓課程",
            "name_en": "ISMS Auditor/Lead Auditor Training Course (BS ISO/IEC 27001:2013)",
            "issuer": "BSI",
            "issue_date": date(2013, 1, 1),
            "certificate_number": "ENR-00792140"
        }
    ]

    for i, cert_data in enumerate(certifications_data, 1):
        certification = Certification(
            name_zh=cert_data["name_zh"],
            name_en=cert_data["name_en"],
            issuer=cert_data["issuer"],
            issue_date=cert_data["issue_date"],
            certificate_number=cert_data["certificate_number"],
            display_order=i
        )
        db.add(certification)

    db.commit()
    print(f"✓ 證照導入完成 ({db.query(Certification).count()} 筆)")


def import_languages(db: Session):
    """導入語言能力"""
    print("\n正在導入語言能力...")

    languages_data = [
        {
            "language_zh": "日文",
            "language_en": "Japanese",
            "proficiency_zh": "N4",
            "proficiency_en": "N4",
            "test_name": "JLPT",
            "score": "N4"
        },
        {
            "language_zh": "英文",
            "language_en": "English",
            "proficiency_zh": "中等",
            "proficiency_en": "Intermediate",
            "test_name": "TOEIC",
            "score": "530"
        }
    ]

    for i, lang_data in enumerate(languages_data, 1):
        language = Language(
            language_zh=lang_data["language_zh"],
            language_en=lang_data["language_en"],
            proficiency_zh=lang_data["proficiency_zh"],
            proficiency_en=lang_data["proficiency_en"],
            test_name=lang_data["test_name"],
            score=lang_data["score"],
            display_order=i
        )
        db.add(language)

    db.commit()
    print(f"✓ 語言能力導入完成 ({db.query(Language).count()} 筆)")


def import_publications(db: Session):
    """導入學術著作"""
    print("\n正在導入學術著作...")

    publications_data = [
        {
            "title": "Framework for NFC-based intelligent agents: a context-awareness enabler for social Internet of things",
            "authors": "Chih-Hao Lin; Pin-Han Ho; Hong-Chuan Lin",
            "publication": "International Journal of Distributed Sensor Networks",
            "year": 2014,
            "pages": "vol.2014, p.1-16"
        },
        {
            "title": "Enhancing Quality of Context Information Through Near Field Communication",
            "authors": "Hong-Chuan Lin",
            "publication": "Chung Yuan Christian University, Dissertation",
            "year": 2011,
            "pages": "p.1-72"
        },
        {
            "title": "The Practical Strategy and Analysis of Adopting Distance Learning Environment in Higher Education",
            "authors": "Chih-Hao Lin, and Hong-Chuan Lin",
            "publication": "GCCCE 2009",
            "year": 2009,
            "pages": "p.935-940"
        }
    ]

    for i, pub_data in enumerate(publications_data, 1):
        publication = Publication(
            title=pub_data["title"],
            authors=pub_data["authors"],
            publication=pub_data["publication"],
            year=pub_data["year"],
            pages=pub_data["pages"],
            display_order=i
        )
        db.add(publication)

    db.commit()
    print(f"✓ 學術著作導入完成 ({db.query(Publication).count()} 筆)")


def import_github_projects(db: Session):
    """導入 GitHub 專案"""
    print("\n正在導入 GitHub 專案...")

    github_projects_data = [
        {
            "name_zh": "Grid Layout Editor (Python 版)",
            "name_en": "Grid Layout Editor (Python Version)",
            "description_zh": "使用 Django 開發的網格佈局編輯器",
            "description_en": "Grid layout editor developed with Django",
            "url": "https://github.com/sprigga/grid_layout_django"
        },
        {
            "name_zh": "Grid Layout Editor (C# 版)",
            "name_en": "Grid Layout Editor (C# Version)",
            "description_zh": "使用 C# 開發的網格佈局編輯器",
            "description_en": "Grid layout editor developed with C#",
            "url": "https://github.com/sprigga/grid_layout_csharp"
        },
        {
            "name_zh": "CAPTCHA CNN 識別系統",
            "name_en": "CAPTCHA CNN Recognition System",
            "description_zh": "使用卷積神經網路進行驗證碼識別",
            "description_en": "CAPTCHA recognition using Convolutional Neural Networks",
            "url": "https://github.com/sprigga/CAPTCHA_CNN"
        },
        {
            "name_zh": "機械故障診斷特徵提取分析",
            "name_en": "Mechanical Fault Diagnosis Feature Extraction Analysis",
            "description_zh": "振動訊號分析與故障診斷系統",
            "description_en": "Vibration signal analysis and fault diagnosis system",
            "url": "https://github.com/sprigga/vibration_signals"
        },
        {
            "name_zh": "台灣股票分析 MCP 伺服器",
            "name_en": "Taiwan Stock Analysis MCP Server",
            "description_zh": "台灣股市數據分析工具",
            "description_en": "Taiwan stock market data analysis tool",
            "url": "https://github.com/sprigga/twstock_analysis?tab=readme-ov-file"
        },
        {
            "name_zh": "台灣彩券 AI 選號系統",
            "name_en": "Taiwan Lottery AI Number Selection System",
            "description_zh": "使用 AI 技術進行台灣彩券號碼分析與選號",
            "description_en": "AI-powered Taiwan lottery number analysis and selection system",
            "url": "https://github.com/sprigga/taiwan_lottery_predict"
        }
    ]

    for i, github_data in enumerate(github_projects_data, 1):
        github_project = GithubProject(
            name_zh=github_data["name_zh"],
            name_en=github_data["name_en"],
            description_zh=github_data["description_zh"],
            description_en=github_data["description_en"],
            url=github_data["url"],
            display_order=i
        )
        db.add(github_project)

    db.commit()
    print(f"✓ GitHub 專案導入完成 ({db.query(GithubProject).count()} 筆)")


def main():
    """主程式"""
    print("=" * 60)
    print("開始導入履歷資料到資料庫")
    print("=" * 60)

    # Create database session
    db = SessionLocal()

    try:
        # 清除現有資料
        clear_existing_data(db)

        # 導入各項資料
        import_personal_info(db)
        work1_id, work2_id, work3_id = import_work_experience(db)
        import_projects(db, work1_id, work2_id, work3_id)
        import_education(db)
        import_certifications(db)
        import_languages(db)  # 新增：導入語言能力
        import_publications(db)
        import_github_projects(db)

        print("\n" + "=" * 60)
        print("✓ 所有履歷資料導入完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 發生錯誤: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
