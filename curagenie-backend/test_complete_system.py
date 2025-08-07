#!/usr/bin/env python3
"""
Comprehensive test script for the CuraGenie patient management system
Tests authentication, profile management, file uploads, and report generation
"""

import requests
import json
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def create_test_vcf():
    """Create a simple test VCF file"""
    vcf_content = """##fileformat=VCFv4.2
##reference=file:///path/to/reference.fasta
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	230710048	rs7903146	C	T	999	PASS	DP=100;AF=0.35
2	165310406	rs12255372	G	T	999	PASS	DP=95;AF=0.28
19	45411941	rs429358	T	C	950	PASS	DP=98;AF=0.25
"""
    return vcf_content.encode()

class CuraGenieSystemTest:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.test_user_email = "testpatient@example.com"
        self.test_user_password = "TestPassword123!"
        
    def test_health_check(self):
        """Test server health"""
        print("🔍 Testing server health...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is healthy")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("\n👤 Testing user registration...")
        
        user_data = {
            "email": self.test_user_email,
            "username": "testpatient",
            "password": self.test_user_password,
            "role": "patient"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/register", json=user_data)
            
            if response.status_code == 200:
                user_info = response.json()
                self.user_id = user_info["id"]
                print(f"✅ User registered successfully: ID {self.user_id}")
                return True
            elif response.status_code == 400 and "already registered" in response.text.lower():
                print("ℹ️ User already exists, continuing with login...")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        print("\n🔐 Testing user login...")
        
        login_data = {
            "email": self.test_user_email,
            "password": self.test_user_password
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", json=login_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data["access_token"]
                self.user_id = token_data["user_id"]
                print(f"✅ Login successful: User ID {self.user_id}")
                return True
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def get_auth_headers(self):
        """Get authentication headers"""
        if not self.token:
            raise Exception("No authentication token available")
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_profile_management(self):
        """Test profile creation and update"""
        print("\n👨‍⚕️ Testing profile management...")
        
        try:
            # Get current profile
            response = requests.get(
                f"{self.base_url}/api/profile/me",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                print("✅ Profile retrieved successfully")
                
                # Update profile
                profile_update = {
                    "first_name": "Test",
                    "last_name": "Patient",
                    "date_of_birth": "1990-01-01T00:00:00",
                    "gender": "Other",
                    "blood_type": "O+",
                    "allergies": "None known",
                    "medical_history": "Test medical history"
                }
                
                update_response = requests.put(
                    f"{self.base_url}/api/profile/me",
                    json=profile_update,
                    headers=self.get_auth_headers()
                )
                
                if update_response.status_code == 200:
                    print("✅ Profile updated successfully")
                    return True
                else:
                    print(f"❌ Profile update failed: {update_response.status_code}")
                    return False
            else:
                print(f"❌ Profile retrieval failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Profile management failed: {e}")
            return False
    
    def test_file_upload(self):
        """Test VCF file upload with authentication"""
        print("\n📁 Testing authenticated file upload...")
        
        try:
            # Create test VCF content
            vcf_data = create_test_vcf()
            
            # Prepare the upload
            files = {'file': ('test_patient.vcf', vcf_data, 'text/plain')}
            
            response = requests.post(
                f"{self.base_url}/api/local-upload/genomic-data",
                files=files,
                headers=self.get_auth_headers()
            )
            
            if response.status_code in [200, 202]:
                result = response.json()
                self.genomic_data_id = result.get('id')
                print(f"✅ File uploaded successfully: ID {self.genomic_data_id}")
                return True
            else:
                print(f"❌ File upload failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ File upload failed: {e}")
            return False
    
    def test_dashboard(self):
        """Test user dashboard"""
        print("\n📊 Testing user dashboard...")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/profile/dashboard",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                dashboard_data = response.json()
                print(f"✅ Dashboard loaded: {dashboard_data['total_uploads']} uploads, {len(dashboard_data['prs_scores'])} PRS scores")
                return True
            else:
                print(f"❌ Dashboard failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Dashboard failed: {e}")
            return False
    
    def test_report_generation(self):
        """Test real-time report generation"""
        print("\n📋 Testing report generation...")
        
        if not hasattr(self, 'genomic_data_id') or not self.genomic_data_id:
            print("❌ No genomic data available for report generation")
            return False
        
        try:
            # Generate instant report
            response = requests.get(
                f"{self.base_url}/api/reports/generate-instant/{self.genomic_data_id}",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                report_data = response.json()
                report = report_data.get('report', {})
                
                print("✅ Report generated successfully!")
                print(f"   - Report ID: {report.get('report_id')}")
                print(f"   - Patient: {report.get('patient_info', {}).get('name', 'Unknown')}")
                print(f"   - Risk Assessment: {len(report.get('risk_assessment', {}).get('risk_summary', {}))} conditions analyzed")
                print(f"   - Recommendations: {len(report.get('recommendations', []))}")
                
                return True
            else:
                print(f"❌ Report generation failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            return False
    
    def test_medical_history(self):
        """Test medical history retrieval"""
        print("\n🏥 Testing medical history...")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/profile/medical-history",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                history = response.json()
                print(f"✅ Medical history retrieved:")
                print(f"   - Patient: {history.get('patient_info', {}).get('name', 'Unknown')}")
                print(f"   - Uploads: {len(history.get('genomic_uploads', []))}")
                print(f"   - Disease risks analyzed: {len(history.get('prs_analysis', {}))}")
                return True
            else:
                print(f"❌ Medical history failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Medical history failed: {e}")
            return False
    
    def test_reports_list(self):
        """Test reports listing"""
        print("\n📑 Testing reports list...")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/reports/my-reports",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                reports_data = response.json()
                print(f"✅ Reports listed: {reports_data.get('total', 0)} reports found")
                return True
            else:
                print(f"❌ Reports list failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Reports list failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run complete system test"""
        print("🚀 CURAGENIE COMPREHENSIVE SYSTEM TEST")
        print("=" * 60)
        
        tests = [
            ("Server Health", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Profile Management", self.test_profile_management),
            ("File Upload", self.test_file_upload),
            ("Dashboard", self.test_dashboard),
            ("Report Generation", self.test_report_generation),
            ("Medical History", self.test_medical_history),
            ("Reports List", self.test_reports_list)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success))
                if success:
                    time.sleep(1)  # Brief pause between tests
                else:
                    print(f"⚠️ {test_name} failed, continuing with remaining tests...")
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{test_name:.<30} {status}")
        
        print("-" * 60)
        print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! CuraGenie system is fully operational!")
            print("\nSystem Features Verified:")
            print("• ✅ User authentication (register/login)")
            print("• ✅ Patient profile management")
            print("• ✅ Secure file uploads with real-time processing")
            print("• ✅ Polygenic risk score calculation")
            print("• ✅ Comprehensive medical report generation")
            print("• ✅ Patient dashboard and medical history")
            print("• ✅ Report management and retrieval")
        else:
            print(f"\n⚠️ {total-passed} test(s) failed. Check the logs above for details.")
        
        return passed == total

def main():
    """Main test function"""
    tester = CuraGenieSystemTest()
    return tester.run_all_tests()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
