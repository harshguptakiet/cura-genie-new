#!/usr/bin/env python3
"""
Test script to diagnose VCF upload issues
"""

import requests
import json
import os
from pathlib import Path

def create_test_vcf():
    """Create a simple test VCF file"""
    vcf_content = """##fileformat=VCFv4.2
##reference=file:///path/to/reference.fasta
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	230710048	rs7903146	C	T	999	PASS	DP=100;AF=0.35
2	165310406	rs12255372	G	T	999	PASS	DP=95;AF=0.28
"""
    return vcf_content.encode()

def test_server_health():
    """Test if the server is responding"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        return False
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_local_upload():
    """Test the local upload endpoint"""
    try:
        # Create test VCF content
        vcf_data = create_test_vcf()
        
        # Prepare the upload
        files = {'file': ('test_sample.vcf', vcf_data, 'text/plain')}
        data = {'user_id': 'test_user_123'}
        
        print("Testing local upload endpoint...")
        response = requests.post(
            "http://localhost:8000/api/local-upload/genomic-data",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 202]:
            result = response.json()
            print("✓ Local upload successful!")
            print(f"Upload ID: {result.get('id')}")
            print(f"Message: {result.get('message')}")
            return True
        else:
            print("✗ Local upload failed!")
            return False
            
    except Exception as e:
        print(f"Local upload test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_s3_upload():
    """Test the S3 upload endpoint (may fail if AWS not configured)"""
    try:
        # Create test VCF content
        vcf_data = create_test_vcf()
        
        # Prepare the upload
        files = {'file': ('test_sample.vcf', vcf_data, 'text/plain')}
        params = {'user_id': 'test_user_123'}
        
        print("Testing S3 upload endpoint...")
        response = requests.post(
            "http://localhost:8000/api/genomic-data/upload",
            files=files,
            params=params,
            timeout=30
        )
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 202]:
            result = response.json()
            print("✓ S3 upload successful!")
            print(f"Upload ID: {result.get('id')}")
            print(f"Message: {result.get('message')}")
            return True
        else:
            print("✗ S3 upload failed (expected if AWS not configured)")
            return False
            
    except Exception as e:
        print(f"S3 upload test failed: {e}")
        return False

def test_upload_endpoints():
    """Test upload endpoint availability"""
    try:
        # Test local upload test endpoint
        response = requests.get("http://localhost:8000/api/local-upload/test", timeout=5)
        print(f"Local upload test endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Endpoint test failed: {e}")
        return False

def check_database():
    """Check if database is accessible"""
    try:
        # Try to get recent uploads
        response = requests.get("http://localhost:8000/api/local-upload/genomic-data/user/test_user_123", timeout=5)
        print(f"Database query: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} uploads for test user")
            return True
        return False
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

def main():
    """Main test function"""
    print("VCF UPLOAD DIAGNOSTIC TEST")
    print("=" * 50)
    
    # Test server health
    print("\n1. Testing server health...")
    if not test_server_health():
        print("❌ Server is not responding. Please start the server first.")
        return 1
    
    # Test endpoints
    print("\n2. Testing upload endpoints...")
    if not test_upload_endpoints():
        print("❌ Upload endpoints not accessible")
        return 1
    
    # Test database
    print("\n3. Testing database connection...")
    check_database()
    
    # Test local upload
    print("\n4. Testing local upload...")
    local_success = test_local_upload()
    
    # Test S3 upload (expected to fail without AWS config)
    print("\n5. Testing S3 upload...")
    s3_success = test_s3_upload()
    
    print("\n" + "=" * 50)
    print("DIAGNOSTIC RESULTS:")
    print(f"✓ Server health: OK")
    print(f"✓ Upload endpoints: OK")
    print(f"{'✓' if local_success else '✗'} Local upload: {'OK' if local_success else 'FAILED'}")
    print(f"{'✓' if s3_success else '✗'} S3 upload: {'OK' if s3_success else 'FAILED (Expected if AWS not configured)'}")
    
    if local_success:
        print("\n🎉 VCF upload is working! The issue might be:")
        print("1. File format/content issues")
        print("2. Frontend-backend communication")
        print("3. File size limits")
        print("4. CORS issues")
    else:
        print("\n❌ VCF upload is failing. Check server logs for details.")
    
    return 0 if local_success else 1

if __name__ == "__main__":
    exit(main())
