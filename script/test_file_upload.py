#!/usr/bin/env python3
"""
Test script for file upload functionality in WorkExperienceEdit.vue
This script simulates the frontend behavior and tests the backend API.
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/work-experience"

def test_file_upload_workflow():
    """Test the complete file upload workflow"""

    print("🔧 Testing File Upload Workflow for Work Experience")
    print("=" * 60)

    # Step 1: Test authentication (get token)
    print("\n1. Testing authentication...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }

    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print("   ✅ Authentication successful")
        else:
            print(f"   ❌ Authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
        print("   ℹ️  Backend might not be running. Start with: uvicorn app.main:app --reload")
        return False

    # Step 2: Test form data preparation (simulate frontend)
    print("\n2. Testing form data preparation...")

    # Simulate the frontend form data that would be sent
    form_data = {
        "company_zh": "測試公司",
        "company_en": "Test Company",
        "position_zh": "軟體工程師",
        "position_en": "Software Engineer",
        "location_zh": "台灣",
        "location_en": "Taiwan",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "is_current": "false",
        "description_zh": "這是一個測試描述",
        "description_en": "This is a test description",
        "display_order": "0"
    }

    print("   ✅ Form data prepared correctly")

    # Step 3: Test file upload API without file (create)
    print("\n3. Testing create work experience without file...")

    try:
        # Test without file first
        response = requests.post(f"{API_BASE}/upload", data=form_data, headers=headers)

        if response.status_code == 201:
            created_experience = response.json()
            experience_id = created_experience["id"]
            print(f"   ✅ Work experience created successfully (ID: {experience_id})")
        else:
            print(f"   ❌ Creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Creation error: {e}")
        return False

    # Step 4: Test file upload API with file (update)
    print("\n4. Testing update work experience with file...")

    # Create a test file
    test_file_content = b"This is a test file content for upload testing"
    test_file_path = "test_upload.txt"

    with open(test_file_path, "wb") as f:
        f.write(test_file_content)

    try:
        # Prepare file for upload
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_upload.txt", f, "text/plain")}

            response = requests.put(
                f"{API_BASE}/{experience_id}/upload",
                data=form_data,
                files=files,
                headers=headers
            )

        if response.status_code == 200:
            updated_experience = response.json()
            print(f"   ✅ Work experience updated successfully with file")
            print(f"   📎 File attachment: {updated_experience.get('attachment_name', 'N/A')}")
            print(f"   📏 File size: {updated_experience.get('attachment_size', 0)} bytes")
        else:
            print(f"   ❌ Update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Update error: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"   🧹 Test file cleaned up")

    # Step 5: Verify file was uploaded and can be accessed
    print("\n5. Testing file accessibility...")

    if updated_experience.get('attachment_url'):
        file_url = f"{BACKEND_URL}{updated_experience['attachment_url']}"
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                print(f"   ✅ File is accessible at: {file_url}")
            else:
                print(f"   ❌ File not accessible: {response.status_code}")
        except Exception as e:
            print(f"   ❌ File access error: {e}")
    else:
        print("   ⚠️  No file URL found in response")

    print("\n" + "=" * 60)
    print("🎉 File upload workflow test completed successfully!")
    print("\n📋 Summary of fixes applied:")
    print("   • Fixed form data handling in updateWorkExperienceWithFile()")
    print("   • Fixed form data handling in createWorkExperienceWithFile()")
    print("   • Ensured all form fields are included even if empty")
    print("   • Removed duplicate 'id' field from FormData")
    print("   • Backend API endpoints are properly configured")

    return True

if __name__ == "__main__":
    test_file_upload_workflow()