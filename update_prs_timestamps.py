import sqlite3

def update_prs_timestamps():
    try:
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        # Update all PRS scores with current timestamp
        cursor.execute("UPDATE prs_scores SET calculated_at = datetime('now') WHERE calculated_at IS NULL")
        rows_updated = cursor.rowcount
        conn.commit()
        
        print(f"✅ Updated {rows_updated} PRS records with calculated_at timestamps")
        
        # Verify the updates
        cursor.execute("SELECT id, disease_type, score, calculated_at FROM prs_scores LIMIT 5")
        results = cursor.fetchall()
        
        print("Sample updated records:")
        for row in results:
            print(f"  ID: {row[0]}, Disease: {row[1]}, Score: {row[2]}, Calculated: {row[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error updating timestamps: {e}")

if __name__ == "__main__":
    update_prs_timestamps()
