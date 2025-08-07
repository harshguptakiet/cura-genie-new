import sqlite3
import json

def test_prs_query():
    try:
        # Connect to the backend database
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        user_id = 1
        print(f"Testing PRS query for user_id: {user_id}")
        
        # Query that the backend might be using
        query = """
        SELECT 
            ps.id,
            ps.genomic_data_id,
            ps.disease_type,
            ps.score,
            gd.filename,
            gd.uploaded_at,
            gd.status
        FROM prs_scores ps
        JOIN genomic_data gd ON ps.genomic_data_id = gd.id
        WHERE gd.user_id = ?
        ORDER BY ps.disease_type
        """
        
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        
        print(f"Query results: {len(results)} records found")
        
        if results:
            print("Sample results:")
            for i, row in enumerate(results[:3]):
                print(f"  {i+1}: {row}")
                
            # Format as JSON like the API would
            formatted_results = []
            for row in results:
                formatted_results.append({
                    "id": row[0],
                    "genomic_data_id": row[1], 
                    "disease_type": row[2],
                    "score": row[3],
                    "filename": row[4],
                    "uploaded_at": row[5],
                    "status": row[6]
                })
            
            print(f"\nJSON response preview:")
            print(json.dumps(formatted_results[:2], indent=2))
        else:
            print("No results found")
            
        # Also test a direct query by user_id string (since genomic_data.user_id might be VARCHAR)
        print(f"\nTesting with user_id as string...")
        cursor.execute(query, (str(user_id),))
        string_results = cursor.fetchall()
        print(f"String query results: {len(string_results)} records found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error in test query: {e}")

if __name__ == "__main__":
    test_prs_query()
