"""
PDF import and data management endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

# 已修改於 2025-12-01，原因：移除不再使用的 subprocess 和 sys 導入
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
# import subprocess  # 不再需要，因為不調用外部 script
# import sys  # 不再需要
from pathlib import Path
import os
import tempfile
from typing import Optional
import shutil
from datetime import datetime

router = APIRouter(prefix="", tags=["Import"])

# 已修改於 2025-12-01，原因：在 Docker 容器中 script 目錄不存在，改為直接調用資料導入函數
# @router.post("/pdf/")
# async def import_pdf(file: UploadFile = File(...), import_type: str = Form("pdf_extraction")):
#     """
#     Upload PDF file and extract resume data
#     """
#     if not file.filename.lower().endswith('.pdf'):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Only PDF files are allowed"
#         )
#
#     try:
#         # For now, we'll call the import_resume_data.py script directly
#         # In the future, we could implement actual PDF text extraction here
#         # Save uploaded PDF to temporary file if needed for processing
#
#         # Execute import_resume_data.py script which has pre-defined sample data
#         # Use absolute path to ensure the script is found regardless of working directory
#         # 已修改於 2025-11-30，原因：修復路徑解析以正確定位項目根目錄（backend/app/api/endpoints -> 回退4層到項目根目錄）
#         project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()  # Go back to project root (5 levels up from import_data.py)
#         script_path = project_root / "script" / "import_resume_data.py"
#
#         # Verify the script exists before running
#         if not script_path.exists():
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Script not found at {script_path}"
#             )
#
#         result = subprocess.run([sys.executable, str(script_path)],
#                                capture_output=True, text=True, timeout=30, cwd=str(project_root))
#
#         if result.returncode != 0:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Script execution failed: {result.stderr}"
#             )
#
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "message": "PDF processed and resume data imported successfully",
#                 "filename": file.filename,
#                 "stdout": result.stdout,
#                 "stderr": result.stderr
#             }
#         )
#     except subprocess.TimeoutExpired:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Script execution timed out"
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error processing PDF: {str(e)}"
#         )

@router.post("/pdf/")
async def import_pdf(file: UploadFile = File(...), import_type: str = Form("pdf_extraction")):
    """
    Upload PDF file and extract resume data
    新版本：直接調用資料庫初始化，不依賴外部 script 目錄
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    try:
        # 已修改於 2025-12-01，原因：完整實現 import_resume_data.py 的所有功能
        from datetime import date
        from sqlalchemy import text
        from app.db.base import SessionLocal
        from app.models.personal_info import PersonalInfo
        from app.models.work_experience import WorkExperience
        from app.models.project import Project, ProjectDetail
        from app.models.education import Education
        from app.models.certification import Certification, Language
        from app.models.publication import Publication, GithubProject

        # 獲取資料庫會話
        db = SessionLocal()

        try:
            # 清除現有資料（保留表結構）
            db.execute(text("DELETE FROM project_details"))
            db.execute(text("DELETE FROM projects"))
            db.execute(text("DELETE FROM work_experience"))
            db.execute(text("DELETE FROM education"))
            db.execute(text("DELETE FROM certifications"))
            db.execute(text("DELETE FROM languages"))
            db.execute(text("DELETE FROM publications"))
            db.execute(text("DELETE FROM github_projects"))
            db.execute(text("DELETE FROM personal_info"))
            db.commit()

            # 1. 導入個人資訊（完整版本）
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

            # 2. 導入工作經歷（4筆）
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

            # 3. 導入教育背景（2筆）
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
                    "description_en": "Project: Ministry of Education's Vehicle Telematics Project",
                    "display_order": 1
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
                    "description_en": "Project: Network Multimedia Related",
                    "display_order": 2
                }
            ]
            for edu_data in education_data:
                education = Education(**edu_data)
                db.add(education)
            db.commit()

            # 4. 導入證照（2筆）
            certifications_data = [
                {
                    "name_zh": "CCNA",
                    "name_en": "CCNA (Cisco Certified Network Associate)",
                    "issuer": "Cisco",
                    "issue_date": date(2007, 1, 1),
                    "certificate_number": "393834169014JOBN",
                    "display_order": 1
                },
                {
                    "name_zh": "ISMS 稽核員/主導稽核員培訓課程",
                    "name_en": "ISMS Auditor/Lead Auditor Training Course (BS ISO/IEC 27001:2013)",
                    "issuer": "BSI",
                    "issue_date": date(2013, 1, 1),
                    "certificate_number": "ENR-00792140",
                    "display_order": 2
                }
            ]
            for cert_data in certifications_data:
                certification = Certification(**cert_data)
                db.add(certification)
            db.commit()

            # 5. 導入語言能力（2筆）
            languages_data = [
                {
                    "language_zh": "日文",
                    "language_en": "Japanese",
                    "proficiency_zh": "N4",
                    "proficiency_en": "N4",
                    "test_name": "JLPT",
                    "score": "N4",
                    "display_order": 1
                },
                {
                    "language_zh": "英文",
                    "language_en": "English",
                    "proficiency_zh": "中等",
                    "proficiency_en": "Intermediate",
                    "test_name": "TOEIC",
                    "score": "530",
                    "display_order": 2
                }
            ]
            for lang_data in languages_data:
                language = Language(**lang_data)
                db.add(language)
            db.commit()

            # 6. 導入學術著作（3筆）
            publications_data = [
                {
                    "title": "Framework for NFC-based intelligent agents: a context-awareness enabler for social Internet of things",
                    "authors": "Chih-Hao Lin; Pin-Han Ho; Hong-Chuan Lin",
                    "publication": "International Journal of Distributed Sensor Networks",
                    "year": 2014,
                    "pages": "vol.2014, p.1-16",
                    "display_order": 1
                },
                {
                    "title": "Enhancing Quality of Context Information Through Near Field Communication",
                    "authors": "Hong-Chuan Lin",
                    "publication": "Chung Yuan Christian University, Dissertation",
                    "year": 2011,
                    "pages": "p.1-72",
                    "display_order": 2
                },
                {
                    "title": "The Practical Strategy and Analysis of Adopting Distance Learning Environment in Higher Education",
                    "authors": "Chih-Hao Lin, and Hong-Chuan Lin",
                    "publication": "GCCCE 2009",
                    "year": 2009,
                    "pages": "p.935-940",
                    "display_order": 3
                }
            ]
            for pub_data in publications_data:
                publication = Publication(**pub_data)
                db.add(publication)
            db.commit()

            # 7. 導入 GitHub 專案（6筆）
            github_projects_data = [
                {
                    "name_zh": "Grid Layout Editor (Python 版)",
                    "name_en": "Grid Layout Editor (Python Version)",
                    "description_zh": "使用 Django 開發的網格佈局編輯器",
                    "description_en": "Grid layout editor developed with Django",
                    "url": "https://github.com/sprigga/grid_layout_django",
                    "display_order": 1
                },
                {
                    "name_zh": "Grid Layout Editor (C# 版)",
                    "name_en": "Grid Layout Editor (C# Version)",
                    "description_zh": "使用 C# 開發的網格佈局編輯器",
                    "description_en": "Grid layout editor developed with C#",
                    "url": "https://github.com/sprigga/grid_layout_csharp",
                    "display_order": 2
                },
                {
                    "name_zh": "CAPTCHA CNN 識別系統",
                    "name_en": "CAPTCHA CNN Recognition System",
                    "description_zh": "使用卷積神經網路進行驗證碼識別",
                    "description_en": "CAPTCHA recognition using Convolutional Neural Networks",
                    "url": "https://github.com/sprigga/CAPTCHA_CNN",
                    "display_order": 3
                },
                {
                    "name_zh": "機械故障診斷特徵提取分析",
                    "name_en": "Mechanical Fault Diagnosis Feature Extraction Analysis",
                    "description_zh": "振動訊號分析與故障診斷系統",
                    "description_en": "Vibration signal analysis and fault diagnosis system",
                    "url": "https://github.com/sprigga/vibration_signals",
                    "display_order": 4
                },
                {
                    "name_zh": "台灣股票分析 MCP 伺服器",
                    "name_en": "Taiwan Stock Analysis MCP Server",
                    "description_zh": "台灣股市數據分析工具",
                    "description_en": "Taiwan stock market data analysis tool",
                    "url": "https://github.com/sprigga/twstock_analysis?tab=readme-ov-file",
                    "display_order": 5
                },
                {
                    "name_zh": "台灣彩券 AI 選號系統",
                    "name_en": "Taiwan Lottery AI Number Selection System",
                    "description_zh": "使用 AI 技術進行台灣彩券號碼分析與選號",
                    "description_en": "AI-powered Taiwan lottery number analysis and selection system",
                    "url": "https://github.com/sprigga/taiwan_lottery_predict",
                    "display_order": 6
                }
            ]
            for github_data in github_projects_data:
                github_project = GithubProject(**github_data)
                db.add(github_project)
            db.commit()

            # 8. 導入專案經驗（使用服務層）
            from app.services.import_resume_service import import_projects_for_work_experience
            project_count, detail_count = import_projects_for_work_experience(
                db, work1.id, work2.id, work3.id
            )

            # 統計導入數量
            stats = {
                "personal_info": 1,
                "work_experience": 4,
                "education": 2,
                "certifications": 2,
                "languages": 2,
                "publications": 3,
                "github_projects": 6,
                "projects": project_count,
                "project_details": detail_count
            }

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "PDF processed and complete resume data imported successfully!",
                    "filename": file.filename,
                    "imported": stats,
                    "total_records": sum(stats.values())
                }
            )
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}\nDetails: {error_detail}"
        )


# 已修改於 2025-12-01，原因：在 Docker 容器中 script 目錄不存在，改為直接執行 SQL
# @router.post("/resume-data/")
# async def import_resume_data():
#     """
#     Import resume data using import_resume_data.py script
#     """
#     try:
#         # Use absolute path to ensure the script is found regardless of working directory
#         # 已修改於 2025-11-30，原因：修復路徑解析以正確定位項目根目錄
#         project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()  # Go back to project root (5 levels up)
#         script_path = project_root / "script" / "import_resume_data.py"
#
#         # Verify the script exists before running
#         if not script_path.exists():
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Script not found at {script_path}"
#             )
#
#         result = subprocess.run([sys.executable, str(script_path)],
#                                capture_output=True, text=True, timeout=30, cwd=str(project_root))
#
#         if result.returncode != 0:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Script execution failed: {result.stderr}"
#             )
#
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "message": "Resume data imported successfully",
#                 "stdout": result.stdout
#             }
#         )
#     except subprocess.TimeoutExpired:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Script execution timed out"
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error importing resume data: {str(e)}"
#         )

@router.post("/resume-data/")
async def import_resume_data():
    """
    Import sample resume data directly (不依賴外部 script)
    """
    try:
        # 導入必要的模組
        from datetime import date
        from app.db.base import SessionLocal
        from app.models.personal_info import PersonalInfo
        from app.models.work_experience import WorkExperience
        from app.models.project import Project, ProjectDetail
        from app.models.education import Education
        from app.models.certification import Certification, Language
        from app.models.publication import Publication, GithubProject
        from sqlalchemy import text

        db = SessionLocal()

        try:
            # 清除現有資料
            db.execute(text("DELETE FROM project_details"))
            db.execute(text("DELETE FROM projects"))
            db.execute(text("DELETE FROM work_experience"))
            db.execute(text("DELETE FROM education"))
            db.execute(text("DELETE FROM certifications"))
            db.execute(text("DELETE FROM languages"))
            db.execute(text("DELETE FROM publications"))
            db.execute(text("DELETE FROM github_projects"))
            db.execute(text("DELETE FROM personal_info"))
            db.commit()

            # 導入個人資訊
            personal_info = PersonalInfo(
                name_zh="林鴻全",
                name_en="Hung Chuan Lin",
                phone="0926-593-172",
                email="sprigga@gmail.com",
                address_zh="台南市安南區北安路三段305巷3號4樓之1",
                address_en="4F.-1, No. 3, Ln. 305, Pei'an Rd., Annan Dist., Tainan City 709004",
                objective_zh="尋求資訊工程師或測試工程師職位，運用豐富的軟體開發經驗與系統整合能力。",
                objective_en="Seeking a position as an IT Customer Engineer or Test Engineer."
            )
            db.add(personal_info)
            db.commit()

            # 返回成功訊息
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Sample resume data imported successfully",
                    "details": "Personal info and basic data have been imported"
                }
            )

        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing resume data: {str(e)}\nDetails: {error_detail}"
        )


# 已註釋於 2025-12-01，原因：此端點依賴 subprocess 和 script 目錄，在容器中不可用
# 資料庫表格會在應用啟動時自動創建，因此此端點不再需要
# @router.post("/database/")
# async def create_database():
#     """
#     Create database tables using create_database.py script
#     """
#     try:
#         # Use absolute path to ensure the script is found regardless of working directory
#         # 已修改於 2025-11-30，原因：修復路徑解析以正確定位項目根目錄
#         project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()  # Go back to project root (5 levels up)
#         script_path = project_root / "script" / "create_database.py"
#
#         # Verify the script exists before running
#         if not script_path.exists():
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Script not found at {script_path}"
#             )
#
#         result = subprocess.run([sys.executable, str(script_path)],
#                                capture_output=True, text=True, timeout=30, cwd=str(project_root))
#
#         if result.returncode != 0:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Database creation failed: {result.stderr}"
#             )
#
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "message": "Database tables created successfully",
#                 "stdout": result.stdout
#             }
#         )
#     except subprocess.TimeoutExpired:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Database creation timed out"
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error creating database: {str(e)}"
#         )


# 已新增於 2025-11-30，原因：新增資料庫匯出功能以方便遷移主機
@router.get("/database/export/")
async def export_database():
    """
    Export the SQLite database file for backup or migration
    """
    try:
        # Get the database file path
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
        db_path = project_root / "backend" / "resume.db"

        # Verify the database file exists
        if not db_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Database file not found at {db_path}"
            )

        # Create a timestamped filename for the export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"resume_db_backup_{timestamp}.db"

        # Return the database file as a download
        return FileResponse(
            path=str(db_path),
            media_type="application/octet-stream",
            filename=export_filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting database: {str(e)}"
        )


# 已新增於 2025-11-30，原因：新增資料庫匯入功能以方便遷移主機
@router.post("/database/import/")
async def import_database(file: UploadFile = File(...)):
    """
    Import a SQLite database file (for restoration or migration)
    WARNING: This will replace the current database!
    """
    if not file.filename.lower().endswith('.db'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .db files are allowed"
        )

    try:
        # Get the database file path
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
        db_path = project_root / "backend" / "resume.db"

        # Create a backup of the current database if it exists
        if db_path.exists():
            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = project_root / "backend" / f"resume_backup_{backup_timestamp}.db"
            shutil.copy2(db_path, backup_path)

        # Save the uploaded database file
        with open(db_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Database imported successfully",
                "filename": file.filename,
                "backup_created": db_path.exists()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing database: {str(e)}"
        )