import requests
import json

def test_upload_directly():
    """Test the upload endpoint directly to see what error occurs"""
    try:
        # Create a test VCF file content
        vcf_content = """##fileformat=VCFv4.2
##source=test
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	sample1
chr1	1000	rs123	A	T	100	PASS	DP=50	GT	0/1
chr1	2000	rs456	G	C	95	PASS	DP=45	GT	1/1
chr2	1500	rs789	C	G	98	PASS	DP=52	GT	0/1"""

        # Create form data
        files = {
            'file': ('test_upload.vcf', vcf_content, 'text/plain')
        }
        
        # Test without authentication first
        print("🧪 Testing upload without authentication...")
        try:
            response = requests.post(
                'http://localhost:8000/api/local-upload/genomic-data',
                files=files,
                timeout=10
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            
        except Exception as e:
            print(f"❌ Upload test error: {e}")
        
        # Test with basic auth headers
        print(f"\n🔑 Testing upload with auth headers...")
        try:
            headers = {
                'Authorization': 'Bearer test-token'
            }
            
            # Recreate files dict because requests consumes it
            files = {
                'file': ('test_upload.vcf', vcf_content, 'text/plain')
            }
            
            response = requests.post(
                'http://localhost:8000/api/local-upload/genomic-data',
                files=files,
                headers=headers,
                timeout=10
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            
        except Exception as e:
            print(f"❌ Auth upload test error: {e}")
    
    except Exception as e:
        print(f"❌ General test error: {e}")

if __name__ == "__main__":
    test_upload_directly()
