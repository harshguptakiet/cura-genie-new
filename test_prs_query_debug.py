import sqlite3
import json

def test_prs_query_debug():
    """Debug the PRS query to see what's causing the 500 error"""
    try:
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        user_id = "1"
        print(f"Testing PRS query for user_id: {user_id}")
        
        # Test the exact query from the API
        query = """
        SELECT ps.id, ps.genomic_data_id, ps.disease_type, ps.score
        FROM prs_scores ps
        JOIN genomic_data gd ON ps.genomic_data_id = gd.id
        WHERE gd.user_id = ?
        ORDER BY ps.disease_type
        """
        
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        
        print(f"Query results: {len(results)} records found")
        
        if results:
            print("PRS results:")
            for row in results:
                print(f"  ID: {row[0]}, GenomicDataID: {row[1]}, Disease: {row[2]}, Score: {row[3]}")
                
            # Format as expected by the API response
            formatted_results = []
            for row in results:
                formatted_results.append({
                    "id": row[0],
                    "genomic_data_id": row[1],
                    "disease_type": row[2],
                    "score": row[3]
                })
            
            print("\nFormatted API response:")
            print(json.dumps(formatted_results, indent=2))
        else:
            print("No PRS results found")
        
        # Also check raw prs_scores table
        print(f"\nDirect prs_scores query:")
        cursor.execute("SELECT * FROM prs_scores ORDER BY id DESC LIMIT 5")
        prs_rows = cursor.fetchall()
        for row in prs_rows:
            print(f"  {row}")
            
        # Check raw genomic_data table
        print(f"\nGenomic data for user {user_id}:")
        cursor.execute("SELECT * FROM genomic_data WHERE user_id = ?", (user_id,))
        genomic_rows = cursor.fetchall()
        for row in genomic_rows:
            print(f"  {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error in PRS query test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prs_query_debug()
