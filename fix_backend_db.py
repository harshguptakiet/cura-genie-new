import sqlite3
from datetime import datetime

def fix_backend_database():
    try:
        # Connect to the backend database
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        # Check current schema
        cursor.execute("PRAGMA table_info(genomic_data)")
        columns = cursor.fetchall()
        
        print("Updated columns in backend database:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Update any existing records that have NULL uploaded_at
        cursor.execute('UPDATE genomic_data SET uploaded_at = datetime("now") WHERE uploaded_at IS NULL')
        rows_updated = cursor.rowcount
        conn.commit()
        
        print(f"✅ Updated {rows_updated} existing records with current timestamp")
        
        # Check if there are any records
        cursor.execute('SELECT COUNT(*) FROM genomic_data')
        count = cursor.fetchone()[0]
        print(f"📊 Total records in genomic_data table: {count}")
        
        conn.close()
        print("🎉 Backend database is now ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_backend_database()
