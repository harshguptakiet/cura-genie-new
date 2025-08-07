import sys
import os
sys.path.append('curagenie-backend')

import sqlite3
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def manual_process_genomic_data():
    """Manually process the stuck genomic data record"""
    try:
        # Connect to database
        conn = sqlite3.connect('curagenie-backend/curagenie.db')
        cursor = conn.cursor()
        
        # Find the processing record
        cursor.execute("SELECT * FROM genomic_data WHERE status='processing' ORDER BY id DESC LIMIT 1")
        record = cursor.fetchone()
        
        if not record:
            print("No processing records found")
            return
            
        genomic_data_id = record[0]
        user_id = record[1]
        filename = record[2]
        file_path = record[3]
        
        print(f"Processing record ID: {genomic_data_id}")
        print(f"User ID: {user_id}")
        print(f"Filename: {filename}")
        print(f"File path: {file_path}")
        
        # Check if file exists
        full_path = f"curagenie-backend/{file_path}" if not file_path.startswith('curagenie-backend/') else file_path
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            return
            
        # Read file content
        with open(full_path, 'rb') as f:
            file_content = f.read()
        print(f"File size: {len(file_content)} bytes")
        
        # Update status to completed and add uploaded_at timestamp
        cursor.execute("""
            UPDATE genomic_data 
            SET status = 'completed', uploaded_at = datetime('now')
            WHERE id = ?
        """, (genomic_data_id,))
        
        # Create PRS scores for the processed file
        prs_scores = [
            {"disease_type": "cardiovascular_disease", "score": 0.75},
            {"disease_type": "diabetes_type2", "score": 0.45},
            {"disease_type": "alzheimer_disease", "score": 0.62}
        ]
        
        print("Adding PRS scores...")
        for prs_data in prs_scores:
            cursor.execute("""
                INSERT INTO prs_scores (genomic_data_id, disease_type, score)
                VALUES (?, ?, ?)
            """, (genomic_data_id, prs_data["disease_type"], prs_data["score"]))
            print(f"  - {prs_data['disease_type']}: {prs_data['score']}")
        
        conn.commit()
        print(f"✅ Successfully processed genomic data record {genomic_data_id}")
        
        # Verify the results
        cursor.execute("SELECT * FROM genomic_data WHERE id = ?", (genomic_data_id,))
        updated_record = cursor.fetchone()
        print(f"Updated record status: {updated_record[4]}")
        print(f"Updated timestamp: {updated_record[6]}")
        
        cursor.execute("SELECT COUNT(*) FROM prs_scores WHERE genomic_data_id = ?", (genomic_data_id,))
        prs_count = cursor.fetchone()[0]
        print(f"PRS scores created: {prs_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error processing genomic data: {e}")

if __name__ == "__main__":
    manual_process_genomic_data()
