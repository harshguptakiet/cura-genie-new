#!/usr/bin/env python3
"""
Test script to verify upload functionality and debug the issue
"""

import requests
import json
import os

def test_upload_endpoint():
    """Test the upload endpoint to see if it's working correctly"""
    print("🧪 Testing CuraGenie Upload Functionality")
    print("=" * 50)
    
    # Test health endpoint first
    try:
        health_response = requests.get("http://localhost:8000/health")
        if health_response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend is not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Test upload endpoint configuration
    try:
        upload_test_response = requests.get("http://localhost:8000/api/local-upload/test")
        if upload_test_response.status_code == 200:
            print("✅ Upload endpoint is configured")
            print(f"📁 Upload directory: {upload_test_response.json()}")
        else:
            print("⚠️  Upload endpoint test failed")
    except Exception as e:
        print(f"⚠️  Upload endpoint test error: {e}")
    
    # Create a test VCF file
    test_vcf_content = '''##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	14370	rs6054257	G	A	29	PASS	NS=3;DP=14;AF=0.5
1	17330	.	T	A	3	q10	NS=3;DP=11;AF=0.017
1	1110696	rs6040355	A	G,T	67	PASS	NS=2;DP=10;AF=0.333,0.667'''
    
    # Write test file
    with open('test_upload.vcf', 'w') as f:
        f.write(test_vcf_content)
    
    print("\n📄 Created test VCF file")
    
    # Test upload (without authentication first)
    try:
        with open('test_upload.vcf', 'rb') as f:
            files = {'file': ('test_upload.vcf', f, 'text/plain')}
            data = {'user_id': '1'}
            
            upload_response = requests.post(
                "http://localhost:8000/api/local-upload/genomic-data",
                files=files,
                data=data
            )
            
            print(f"\n🚀 Upload attempt status: {upload_response.status_code}")
            
            if upload_response.status_code == 202:
                print("✅ Upload successful!")
                print(f"📋 Response: {upload_response.json()}")
            elif upload_response.status_code == 401:
                print("🔐 Authentication required (expected for this endpoint)")
                print(f"📋 Response: {upload_response.json()}")
            else:
                print(f"⚠️  Upload failed: {upload_response.status_code}")
                print(f"📋 Response: {upload_response.text}")
                
    except Exception as e:
        print(f"❌ Upload error: {e}")
    
    # Clean up
    if os.path.exists('test_upload.vcf'):
        os.remove('test_upload.vcf')
        print("\n🧹 Cleaned up test file")
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSIS:")
    print("1. If upload succeeded (202), the backend is working fine")
    print("2. If authentication error (401), that's normal - need login")
    print("3. The issue is likely in the frontend state management")
    print("4. The fix I implemented should resolve the upload reset issue")

if __name__ == "__main__":
    test_upload_endpoint()
