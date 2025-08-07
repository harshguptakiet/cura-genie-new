import sqlite3

def analyze_prs_scores():
    """Analyze the PRS scores to understand why there are duplicates"""
    try:
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        # Get all PRS scores for user 1 with details
        query = """
        SELECT 
            ps.id,
            ps.genomic_data_id,
            ps.disease_type,
            ps.score,
            ps.calculated_at,
            gd.filename,
            gd.uploaded_at,
            gd.status
        FROM prs_scores ps
        JOIN genomic_data gd ON ps.genomic_data_id = gd.id
        WHERE gd.user_id = '1'
        ORDER BY ps.disease_type, ps.genomic_data_id
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print("📊 Current PRS scores in database:")
        print("=" * 80)
        
        current_disease = None
        for row in rows:
            prs_id, genomic_id, disease, score, calc_time, filename, upload_time, status = row
            
            if disease != current_disease:
                print(f"\n🔬 Disease: {disease}")
                current_disease = disease
            
            print(f"  📋 ID:{prs_id}, File:{genomic_id} ({filename}), Score:{score}, Status:{status}")
        
        print(f"\n📈 Summary:")
        
        # Count by disease type
        cursor.execute("""
            SELECT ps.disease_type, COUNT(*) as count
            FROM prs_scores ps
            JOIN genomic_data gd ON ps.genomic_data_id = gd.id
            WHERE gd.user_id = '1'
            GROUP BY ps.disease_type
            ORDER BY ps.disease_type
        """)
        
        disease_counts = cursor.fetchall()
        for disease, count in disease_counts:
            print(f"  - {disease}: {count} records")
        
        # Count by genomic data file
        cursor.execute("""
            SELECT gd.id, gd.filename, gd.status, COUNT(ps.id) as prs_count
            FROM genomic_data gd
            LEFT JOIN prs_scores ps ON gd.id = ps.genomic_data_id
            WHERE gd.user_id = '1'
            GROUP BY gd.id, gd.filename, gd.status
            ORDER BY gd.id
        """)
        
        file_counts = cursor.fetchall()
        print(f"\n📁 Genomic files and their PRS scores:")
        for file_id, filename, status, prs_count in file_counts:
            print(f"  - File {file_id} ({filename}): {prs_count} PRS scores, Status: {status}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error analyzing PRS scores: {e}")

if __name__ == "__main__":
    analyze_prs_scores()
