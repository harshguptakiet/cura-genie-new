import requests
import json

def test_api_endpoints():
    """Test all the key API endpoints to verify they're working"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        {
            "name": "Upload Test Endpoint", 
            "url": f"{base_url}/api/local-upload/test",
            "method": "GET"
        },
        {
            "name": "PRS Scores for User 1", 
            "url": f"{base_url}/api/prs/scores/user/1",
            "method": "GET"
        },
        {
            "name": "PRS Scores for Latest Upload (genomic_data_id=4)", 
            "url": f"{base_url}/api/prs/scores/genomic-data/4",
            "method": "GET"
        },
        {
            "name": "Genomic Data for User 1", 
            "url": f"{base_url}/api/local-upload/genomic-data/user/1",
            "method": "GET"
        }
    ]
    
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            print(f"\n📡 Testing: {endpoint['name']}")
            
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                
                # Show sample data based on endpoint
                if "prs/scores" in endpoint['url']:
                    print(f"📊 Found {len(data)} PRS scores")
                    if data:
                        print(f"   Sample: {data[0]['disease_type']} = {data[0]['score']}")
                elif "genomic-data/user" in endpoint['url']:
                    print(f"🧬 Found {len(data)} genomic data records")
                    if data:
                        print(f"   Latest: {data[-1]['filename']} ({data[-1]['status']})")
                else:
                    print(f"📝 Response: {json.dumps(data, indent=2)[:200]}...")
                    
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    test_api_endpoints()
