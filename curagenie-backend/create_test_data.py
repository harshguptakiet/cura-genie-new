#!/usr/bin/env python3
"""
Create test data for user 3
"""
from db.database import get_db
from db.models import GenomicData, PrsScore
from datetime import datetime

session = next(get_db())
try:
    # Create genomic data for user 3
    genomic_file = GenomicData(
        user_id='3',  # String format as expected by the API
        filename='test_sample.vcf',
        file_url='uploads/test_sample.vcf',
        status='completed',
        metadata_json='{"size": "2MB", "variants": 150}',
        uploaded_at=datetime.now()
    )
    
    session.add(genomic_file)
    session.commit()
    session.refresh(genomic_file)
    
    # Create some PRS scores
    prs_diseases = ['cardiovascular_disease', 'diabetes_type2', 'alzheimer_disease']
    scores = [0.65, 0.42, 0.78]
    
    for disease, score in zip(prs_diseases, scores):
        prs = PrsScore(
            genomic_data_id=genomic_file.id,
            disease_type=disease,
            score=score,
            calculated_at=datetime.now()
        )
        session.add(prs)
    
    session.commit()
    print(f'✅ Created test data for user 3')
    print(f'📁 Genomic file ID: {genomic_file.id}')
    print(f'📊 Created {len(prs_diseases)} PRS scores')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
finally:
    session.close()
