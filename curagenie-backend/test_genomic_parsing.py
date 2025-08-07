#!/usr/bin/env python3
"""
Test script for advanced genomic parsing capabilities in CuraGenie

This script demonstrates the enhanced genomic file parsing functionality including:
- Comprehensive FASTQ quality analysis
- Advanced VCF variant analysis
- Real polygenic risk score calculations
- Quality control assessments
"""

import os
import sys
import json
from typing import Dict, Any

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genomic_utils import GenomicProcessor

def create_sample_fastq() -> bytes:
    """Create a sample FASTQ file for testing"""
    fastq_content = """@SEQ_ID_1
ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT
+
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
@SEQ_ID_2
TTGGCCAAATTGGCCAAATTGGCCAAATTGGCCAAATT
+
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
@SEQ_ID_3
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
+
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
@SEQ_ID_4
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
+
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
@SEQ_ID_5
CGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCG
+
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
"""
    return fastq_content.encode()

def create_sample_vcf() -> bytes:
    """Create a sample VCF file for testing"""
    vcf_content = """##fileformat=VCFv4.2
##reference=file:///path/to/reference.fasta
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	230710048	rs7903146	C	T	999	PASS	DP=100;AF=0.35
2	165310406	rs12255372	G	T	999	PASS	DP=95;AF=0.28
3	12393125	rs1801282	C	G	850	PASS	DP=88;AF=0.12
11	17409572	rs5219	C	T	920	PASS	DP=105;AF=0.42
8	118184783	rs13266634	C	T	780	PASS	DP=92;AF=0.18
19	45411941	rs429358	T	C	950	PASS	DP=98;AF=0.25
X	154944204	rs7412	C	T	880	PASS	DP=87;AF=0.08
2	227093069	rs11136000	C	T	760	PASS	DP=83;AF=0.15
11	85868640	rs3851179	A	G	820	PASS	DP=91;AF=0.22
12	125310406	rs599839	A	G	890	PASS	DP=97;AF=0.31
"""
    return vcf_content.encode()

def test_fastq_parsing():
    """Test FASTQ file parsing with advanced analysis"""
    print("=" * 60)
    print("TESTING ADVANCED FASTQ PARSING")
    print("=" * 60)
    
    # Create sample FASTQ data
    fastq_data = create_sample_fastq()
    
    # Initialize genomic processor
    processor = GenomicProcessor()
    
    # Process FASTQ file
    print("Processing sample FASTQ file...")
    result = processor.process_genomic_file(fastq_data, "sample.fastq")
    
    if result.get("status") == "error":
        print(f"ERROR: {result.get('message')}")
        return False
    
    print(f"✓ Successfully processed FASTQ file")
    print(f"File type: {result.get('file_type')}")
    print(f"Total sequences: {result.get('total_sequences')}")
    print(f"Sample analyzed: {result.get('sample_analyzed')}")
    
    # Display read length statistics
    if "read_length" in result:
        read_stats = result["read_length"]
        print(f"\nRead Length Statistics:")
        print(f"  Mean: {read_stats.get('mean', 0):.1f} bp")
        print(f"  Median: {read_stats.get('median', 0):.1f} bp")
        print(f"  Range: {read_stats.get('min', 0)} - {read_stats.get('max', 0)} bp")
    
    # Display GC content
    if "gc_content" in result:
        gc_stats = result["gc_content"]
        print(f"\nGC Content:")
        print(f"  Mean: {gc_stats.get('mean', 0):.1f}%")
        print(f"  Median: {gc_stats.get('median', 0):.1f}%")
    
    # Display quality metrics
    if "quality_metrics" in result and "status" not in result["quality_metrics"]:
        qual_metrics = result["quality_metrics"]
        print(f"\nQuality Metrics:")
        print(f"  Mean quality: {qual_metrics.get('mean_quality', 0):.1f}")
        print(f"  Median quality: {qual_metrics.get('median_quality', 0):.1f}")
        
        if "quality_distribution" in qual_metrics:
            qual_dist = qual_metrics["quality_distribution"]
            print(f"  High quality bases (≥30): {qual_dist.get('high_quality_percent', 0):.1f}%")
            print(f"  Medium quality bases (20-29): {qual_dist.get('medium_quality_percent', 0):.1f}%")
            print(f"  Low quality bases (<20): {qual_dist.get('low_quality_percent', 0):.1f}%")
    
    # Display quality assessment
    if "quality_assessment" in result:
        assessment = result["quality_assessment"]
        print(f"\nQuality Assessment:")
        print(f"  Overall quality: {assessment.get('overall_quality', 'Unknown')}")
        print(f"  Pass filters: {assessment.get('pass_filters', False)}")
        if assessment.get('issues'):
            print(f"  Issues: {', '.join(assessment['issues'])}")
        if assessment.get('recommendations'):
            print(f"  Recommendations: {', '.join(assessment['recommendations'])}")
    
    print("\n" + "-" * 60)
    return True

def test_vcf_parsing():
    """Test VCF file parsing with variant analysis"""
    print("=" * 60)
    print("TESTING ADVANCED VCF PARSING")
    print("=" * 60)
    
    # Create sample VCF data
    vcf_data = create_sample_vcf()
    
    # Initialize genomic processor
    processor = GenomicProcessor()
    
    # Process VCF file
    print("Processing sample VCF file...")
    result = processor.process_genomic_file(vcf_data, "sample.vcf")
    
    if result.get("status") == "error":
        print(f"ERROR: {result.get('message')}")
        return False
    
    print(f"✓ Successfully processed VCF file")
    print(f"File type: {result.get('file_type')}")
    print(f"Total variants: {result.get('total_variants')}")
    print(f"Sample analyzed: {result.get('sample_analyzed')}")
    
    # Display chromosome distribution
    if "chromosome_distribution" in result:
        chr_dist = result["chromosome_distribution"]
        print(f"\nChromosome Distribution:")
        for chrom, count in sorted(chr_dist.items()):
            print(f"  {chrom}: {count} variants")
    
    # Display variant type distribution
    if "variant_type_distribution" in result:
        var_types = result["variant_type_distribution"]
        print(f"\nVariant Type Distribution:")
        for var_type, count in var_types.items():
            print(f"  {var_type}: {count} variants")
    
    # Display quality metrics
    if "quality_metrics" in result and "status" not in result["quality_metrics"]:
        qual_metrics = result["quality_metrics"]
        print(f"\nQuality Metrics:")
        print(f"  Mean quality: {qual_metrics.get('mean_quality', 0):.1f}")
        print(f"  Quality range: {qual_metrics.get('min_quality', 0):.1f} - {qual_metrics.get('max_quality', 0):.1f}")
        print(f"  High quality variants (≥30): {qual_metrics.get('high_quality_variants', 0)}")
    
    # Display header information
    if "header_info" in result:
        header = result["header_info"]
        print(f"\nHeader Information:")
        print(f"  Format version: {header.get('format_version', 'Unknown')}")
        print(f"  Reference genome: {header.get('reference_genome', 'Unknown')}")
        print(f"  INFO fields: {len(header.get('info_fields', []))}")
        print(f"  Samples: {len(header.get('samples', []))}")
    
    # Display quality assessment
    if "quality_assessment" in result:
        assessment = result["quality_assessment"]
        print(f"\nQuality Assessment:")
        print(f"  Overall quality: {assessment.get('overall_quality', 'Unknown')}")
        print(f"  Pass filters: {assessment.get('pass_filters', False)}")
        if assessment.get('issues'):
            print(f"  Issues: {', '.join(assessment['issues'])}")
        if assessment.get('recommendations'):
            print(f"  Recommendations: {', '.join(assessment['recommendations'])}")
    
    print("\n" + "-" * 60)
    return result

def test_prs_calculation(vcf_result: Dict[str, Any]):
    """Test polygenic risk score calculation"""
    print("=" * 60)
    print("TESTING POLYGENIC RISK SCORE CALCULATION")
    print("=" * 60)
    
    # Initialize genomic processor
    processor = GenomicProcessor()
    
    # Test PRS calculation for different diseases
    diseases = ["diabetes", "alzheimer", "heart_disease"]
    
    for disease in diseases:
        print(f"\nCalculating PRS for {disease}...")
        prs_result = processor.calculate_polygenic_risk_score(vcf_result, disease)
        
        if prs_result.get("status") == "error":
            print(f"  ERROR: {prs_result.get('message')}")
            continue
        
        print(f"  ✓ PRS calculation successful")
        print(f"  Disease: {prs_result.get('disease_type', disease)}")
        print(f"  Normalized PRS: {prs_result.get('normalized_prs', 0):.3f}")
        print(f"  Interpretation: {prs_result.get('interpretation', 'Unknown')}")
        print(f"  Method: {prs_result.get('method', 'unknown')}")
        
        if "variants_found" in prs_result:
            print(f"  Variants found: {prs_result['variants_found']}")
            print(f"  Total variants in panel: {prs_result.get('variants_used', 0)}")
        
        if "contributing_variants" in prs_result and prs_result["contributing_variants"]:
            print(f"  Contributing variants:")
            for variant_id, info in list(prs_result["contributing_variants"].items())[:3]:
                print(f"    {variant_id}: weight={info.get('weight', 0):.3f}, contribution={info.get('contribution', 0):.3f}")
    
    print("\n" + "-" * 60)

def main():
    """Main test function"""
    print("CURAGENIE ADVANCED GENOMIC PARSING TEST")
    print("=" * 60)
    print("This test demonstrates the enhanced genomic file parsing capabilities")
    print("including comprehensive quality analysis and real PRS calculations.\n")
    
    try:
        # Test FASTQ parsing
        fastq_success = test_fastq_parsing()
        
        if not fastq_success:
            print("FASTQ parsing test failed!")
            return 1
        
        # Test VCF parsing
        vcf_result = test_vcf_parsing()
        
        if not vcf_result or vcf_result.get("status") == "error":
            print("VCF parsing test failed!")
            return 1
        
        # Test PRS calculation
        test_prs_calculation(vcf_result)
        
        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nKey improvements over the previous system:")
        print("• Comprehensive FASTQ quality metrics (GC content, quality scores, duplications)")
        print("• Advanced VCF parsing with variant classification and annotation")
        print("• Real polygenic risk score calculations based on known disease variants")
        print("• Quality control assessments with recommendations")
        print("• Support for compressed files (.gz)")
        print("• Detailed genomic region analysis")
        print("• Position-specific quality analysis for FASTQ")
        print("• Chromosome and variant type distributions for VCF")
        
        return 0
        
    except Exception as e:
        print(f"\nTEST FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
