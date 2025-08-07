import requests
import json

def test_auth_and_upload():
    """Test authentication and then upload"""
    try:
        # Test authentication first
        print("🔑 Testing authentication...")
        
        login_data = {
            "email": "guptasecular1@gmail.com",
            "password": "patient1",  # This might need to be the actual password
            "remember_me": False
        }
        
        # Try to login
        login_response = requests.post(
            'http://localhost:8000/api/auth/login',
            json=login_data,
            timeout=10
        )
        
        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text[:300]}...")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get('access_token')
            print(f"✅ Got token: {token[:50]}..." if token else "❌ No token received")
            
            if token:
                # Now test upload with valid token
                print(f"\n📤 Testing upload with valid token...")
                
                vcf_content = """##fileformat=VCFv4.2
##source=test
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	sample1
chr1	1000	rs123	A	T	100	PASS	DP=50	GT	0/1
chr1	2000	rs456	G	C	95	PASS	DP=45	GT	1/1
chr2	1500	rs789	C	G	98	PASS	DP=52	GT	0/1"""

                files = {
                    'file': ('test_upload.vcf', vcf_content, 'text/plain')
                }
                
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                
                upload_response = requests.post(
                    'http://localhost:8000/api/local-upload/genomic-data',
                    files=files,
                    headers=headers,
                    timeout=15
                )
                
                print(f"Upload Status: {upload_response.status_code}")
                print(f"Upload Response: {upload_response.text}")
                
            else:
                print("❌ Cannot test upload without valid token")
        else:
            print("❌ Authentication failed, cannot test upload")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_auth_and_upload()
