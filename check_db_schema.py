import sqlite3
import datetime

def check_and_fix_database():
    try:
        # Connect to the database
        conn = sqlite3.connect('curagenie.db')
        cursor = conn.cursor()
        
        # Check if genomic_data table exists
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='genomic_data'")
        result = cursor.fetchone()
        
        if result:
            print("Current genomic_data table schema:")
            print(result[0])
            print()
            
            # Check if uploaded_at column exists
            cursor.execute("PRAGMA table_info(genomic_data)")
            columns = cursor.fetchall()
            
            print("Current columns:")
            column_names = []
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
                column_names.append(col[1])
            
            # Check if uploaded_at exists
            if 'uploaded_at' not in column_names:
                print("\nMISSING: uploaded_at column not found!")
                print("Attempting to add uploaded_at column...")
                
                try:
                    # Add the missing column with a default timestamp
                    cursor.execute("ALTER TABLE genomic_data ADD COLUMN uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                    conn.commit()
                    print("✅ Successfully added uploaded_at column!")
                    
                    # Update existing records to have uploaded_at values
                    cursor.execute("UPDATE genomic_data SET uploaded_at = CURRENT_TIMESTAMP WHERE uploaded_at IS NULL")
                    conn.commit()
                    print("✅ Updated existing records with current timestamp")
                    
                except Exception as e:
                    print(f"❌ Error adding column: {e}")
            else:
                print("\n✅ uploaded_at column already exists!")
                
        else:
            print("❌ genomic_data table not found!")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("Checking database schema...")
    check_and_fix_database()
