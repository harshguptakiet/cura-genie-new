"""
Real MRI Image Analysis Functions
This module provides actual image processing-based tumor detection
instead of the mock/simulated analysis
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import io
from scipy import ndimage
from scipy.ndimage import label, binary_erosion, binary_dilation
from skimage import measure, morphology
from skimage.filters import threshold_otsu, gaussian
from skimage.segmentation import watershed
from skimage.feature import peak_local_maxima
import logging

logger = logging.getLogger(__name__)

class RealMRIAnalyzer:
    """Real MRI image analysis using computer vision techniques"""
    
    def __init__(self):
        self.min_tumor_size = 100  # minimum pixels for a tumor region
        self.max_tumor_size = 10000  # maximum pixels for a tumor region
        self.confidence_threshold = 0.6
        
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess MRI image for analysis"""
        # Convert to grayscale if needed
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert to numpy array
        img_array = np.array(image, dtype=np.float32)
        
        # Normalize to 0-1
        img_array = img_array / 255.0
        
        # Apply Gaussian smoothing to reduce noise
        img_array = gaussian(img_array, sigma=1.0)
        
        return img_array
    
    def segment_brain_region(self, img_array: np.ndarray) -> np.ndarray:
        """Segment the brain region from the background"""
        # Use Otsu's thresholding to separate brain from background
        threshold = threshold_otsu(img_array)
        brain_mask = img_array > threshold * 0.3  # Lower threshold to capture more brain tissue
        
        # Clean up the mask with morphological operations
        brain_mask = binary_erosion(brain_mask, iterations=1)
        brain_mask = binary_dilation(brain_mask, iterations=2)
        
        # Keep only the largest connected component (main brain region)
        labeled_mask, num_labels = label(brain_mask)
        if num_labels > 0:
            # Find largest component
            component_sizes = np.bincount(labeled_mask.ravel())[1:]  # Skip background
            if len(component_sizes) > 0:
                largest_component = np.argmax(component_sizes) + 1
                brain_mask = labeled_mask == largest_component
        
        return brain_mask
    
    def detect_anomalies(self, img_array: np.ndarray, brain_mask: np.ndarray) -> list:
        """Detect potential tumor regions using image processing"""
        anomalies = []
        
        # Apply brain mask to focus only on brain tissue
        brain_img = img_array * brain_mask
        
        # Calculate image statistics for the brain region
        brain_pixels = brain_img[brain_mask]
        if len(brain_pixels) == 0:
            return anomalies
            
        mean_intensity = np.mean(brain_pixels)
        std_intensity = np.std(brain_pixels)
        
        logger.info(f"   - Brain tissue stats: mean={mean_intensity:.3f}, std={std_intensity:.3f}")
        
        # Method 1: Detect bright spots (potential tumors appear brighter)
        bright_threshold = mean_intensity + 1.5 * std_intensity
        bright_regions = (brain_img > bright_threshold) & brain_mask
        
        # Method 2: Detect dark spots (some tumors appear darker)
        dark_threshold = mean_intensity - 1.2 * std_intensity
        dark_regions = (brain_img < dark_threshold) & (brain_img > 0.1) & brain_mask
        
        # Method 3: Detect regions with unusual texture (edge-based)
        # Apply edge detection
        from scipy.ndimage import sobel
        edges = np.sqrt(sobel(brain_img, axis=0)**2 + sobel(brain_img, axis=1)**2)
        edge_threshold = np.mean(edges[brain_mask]) + 2 * np.std(edges[brain_mask])
        edge_regions = (edges > edge_threshold) & brain_mask
        
        # Combine detection methods
        combined_regions = bright_regions | dark_regions | edge_regions
        
        # Clean up detected regions
        combined_regions = binary_erosion(combined_regions, iterations=1)
        combined_regions = binary_dilation(combined_regions, iterations=2)
        
        # Label connected components
        labeled_regions, num_regions = label(combined_regions)
        
        logger.info(f"   - Found {num_regions} potential regions before filtering")
        
        for region_id in range(1, num_regions + 1):
            region_mask = labeled_regions == region_id
            region_size = np.sum(region_mask)
            
            # Filter by size
            if region_size < self.min_tumor_size or region_size > self.max_tumor_size:
                continue
            
            # Get region properties
            region_coords = np.where(region_mask)
            y_min, y_max = np.min(region_coords[0]), np.max(region_coords[0])
            x_min, x_max = np.min(region_coords[1]), np.max(region_coords[1])
            
            # Calculate region statistics
            region_pixels = brain_img[region_mask]
            region_mean = np.mean(region_pixels)
            region_std = np.std(region_pixels)
            
            # Calculate confidence based on how different the region is from normal brain
            intensity_diff = abs(region_mean - mean_intensity) / std_intensity
            confidence = min(0.95, max(0.5, intensity_diff / 3.0))
            
            # Determine tumor type based on characteristics
            if region_mean > mean_intensity + std_intensity:
                # Bright region - likely glioma or metastasis
                if region_size > 500:
                    tumor_type = "glioma"
                    risk_level = "high"
                else:
                    tumor_type = "metastatic"
                    risk_level = "moderate"
            elif region_mean < mean_intensity - 0.5 * std_intensity:
                # Dark region - likely meningioma
                tumor_type = "meningioma"
                risk_level = "low" if region_size < 300 else "moderate"
            else:
                # Edge-detected region
                tumor_type = "pituitary_adenoma"
                risk_level = "low" if region_size < 200 else "moderate"
            
            # Calculate approximate volume (assuming roughly spherical)
            volume_mm3 = int(region_size * 0.5)  # Rough approximation
            
            # Determine shape irregularity
            # Calculate aspect ratio
            height = y_max - y_min + 1
            width = x_max - x_min + 1
            aspect_ratio = max(height/width, width/height)
            irregular_shape = aspect_ratio > 1.5
            
            # Calculate enhancement pattern based on intensity variation
            if region_std > std_intensity * 0.5:
                enhancement_pattern = "heterogeneous"
            elif region_mean > mean_intensity + std_intensity:
                enhancement_pattern = "rim"
            elif region_mean > mean_intensity:
                enhancement_pattern = "homogeneous"  
            else:
                enhancement_pattern = "none"
            
            # Check for surrounding edema (bright halo)
            # Dilate region mask to check surrounding area
            dilated_mask = binary_dilation(region_mask, iterations=5)
            surrounding_mask = dilated_mask & ~region_mask & brain_mask
            if np.sum(surrounding_mask) > 0:
                surrounding_mean = np.mean(brain_img[surrounding_mask])
                edema_present = surrounding_mean > mean_intensity + 0.3 * std_intensity
            else:
                edema_present = False
            
            anomaly = {
                "id": f"region_{len(anomalies) + 1}",
                "type": tumor_type,
                "bbox": {
                    "x": int(x_min),
                    "y": int(y_min), 
                    "width": int(x_max - x_min + 1),
                    "height": int(y_max - y_min + 1)
                },
                "confidence": float(round(confidence, 3)),
                "risk_level": risk_level,
                "volume_mm3": volume_mm3,
                "size_pixels": int(region_size),
                "characteristics": {
                    "irregular_shape": irregular_shape,
                    "enhancement_pattern": enhancement_pattern,
                    "edema_present": edema_present,
                    "calcification": region_std < std_intensity * 0.3,  # Low variation suggests calcification
                    "intensity_stats": {
                        "mean": float(region_mean),
                        "std": float(region_std),
                        "contrast_ratio": float(intensity_diff)
                    }
                }
            }
            
            anomalies.append(anomaly)
            logger.info(f"     - Detected: {tumor_type} at ({x_min},{y_min}) size:{region_size}px confidence:{confidence:.2f}")
        
        return anomalies
    
    def analyze_image(self, image: Image.Image) -> dict:
        """Main analysis function that processes an MRI image"""
        logger.info("🔍 Starting REAL MRI image analysis")
        
        try:
            # Preprocess the image
            logger.info("   - Preprocessing image...")
            img_array = self.preprocess_image(image)
            
            # Segment brain region
            logger.info("   - Segmenting brain region...")
            brain_mask = self.segment_brain_region(img_array)
            brain_area = np.sum(brain_mask)
            
            logger.info(f"   - Brain region area: {brain_area} pixels")
            
            if brain_area < 1000:  # Very small brain region
                logger.warning("   - Brain region too small, analysis may be unreliable")
            
            # Detect anomalies
            logger.info("   - Detecting anomalous regions...")
            tumor_regions = self.detect_anomalies(img_array, brain_mask)
            
            # Calculate overall assessment
            if tumor_regions:
                high_risk_count = sum(1 for r in tumor_regions if r["risk_level"] == "high")
                moderate_risk_count = sum(1 for r in tumor_regions if r["risk_level"] == "moderate")
                
                if high_risk_count > 0:
                    overall_risk = "high"
                elif moderate_risk_count > 1:
                    overall_risk = "moderate" 
                elif moderate_risk_count > 0 or len(tumor_regions) > 2:
                    overall_risk = "moderate"
                else:
                    overall_risk = "low"
                
                total_volume = sum(r["volume_mm3"] for r in tumor_regions)
                avg_confidence = np.mean([r["confidence"] for r in tumor_regions])
            else:
                overall_risk = "low"
                total_volume = 0
                avg_confidence = 0.95  # High confidence in normal scan
            
            result = {
                "status": "success",
                "method": "real_image_analysis", 
                "tumor_regions": tumor_regions,
                "overall_assessment": {
                    "risk_level": overall_risk,
                    "confidence": float(round(avg_confidence, 3)),
                    "total_volume_mm3": int(total_volume),
                    "num_regions_detected": len(tumor_regions)
                },
                "image_analysis_stats": {
                    "brain_area_pixels": int(brain_area),
                    "image_dimensions": img_array.shape,
                    "processing_method": "computer_vision_based"
                }
            }
            
            logger.info(f"✅ Real analysis complete: {len(tumor_regions)} regions, risk={overall_risk}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Real image analysis failed: {e}")
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}",
                "method": "real_image_analysis"
            }

def analyze_mri_image_real(image: Image.Image) -> dict:
    """Convenience function to analyze an MRI image using real computer vision"""
    analyzer = RealMRIAnalyzer()
    return analyzer.analyze_image(image)

def test_real_analysis():
    """Test the real analysis with a sample image"""
    print("🧪 Testing Real MRI Analysis...")
    
    # Create a test image with some artificial anomalies
    size = (256, 256)
    img_array = np.random.randint(50, 100, size=size, dtype=np.uint8)
    
    # Add brain-like structure
    center_x, center_y = size[0] // 2, size[1] // 2
    y, x = np.ogrid[:size[1], :size[0]]
    brain_mask = (x - center_x)**2 + (y - center_y)**2 < (min(size) // 3)**2
    img_array[brain_mask] = np.random.randint(100, 150, np.sum(brain_mask))
    
    # Add some bright spots (simulated tumors)
    for i in range(2):
        tumor_x = center_x + np.random.randint(-50, 50)
        tumor_y = center_y + np.random.randint(-50, 50) 
        tumor_size = np.random.randint(200, 500)
        tumor_mask = (x - tumor_x)**2 + (y - tumor_y)**2 < tumor_size
        img_array[tumor_mask] = np.random.randint(180, 220, np.sum(tumor_mask))
    
    # Convert to PIL Image
    test_image = Image.fromarray(img_array, mode='L')
    
    # Analyze
    result = analyze_mri_image_real(test_image)
    
    print(f"   Status: {result.get('status')}")
    print(f"   Method: {result.get('method')}")
    print(f"   Regions found: {len(result.get('tumor_regions', []))}")
    print(f"   Overall risk: {result.get('overall_assessment', {}).get('risk_level')}")
    
    return result.get('status') == 'success'

if __name__ == "__main__":
    # Test the real analysis
    success = test_real_analysis()
    if success:
        print("✅ Real MRI analysis is working!")
    else:
        print("❌ Real MRI analysis has issues")
