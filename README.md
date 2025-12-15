# ECE253 Image Processing Project

Scripting and automating image processing techniques on photos of Daphnia (D. magna).

## Installation & Setup

### Clone Repository with Submodules

```bash
git clone --recurse-submodules <repository-url>
cd ECE253
```

### Dataset

Download the dataset from this [Google Drive link](https://drive.google.com/file/d/16f5vKlTksrY68vdscSIL6Uj8a39R3CHN/view?usp=sharing) (please sign in with UCSD credentials) and unzip it into the repository root. The dataset contains pre-converted PNG images ready for processing.

## Requirements

Install required Python packages:
```bash
pip install opencv-python numpy matplotlib pandas rawpy imageio scikit-image
```

## Usage

### 1. Low-Light Enhancement

#### CLAHE Method

Apply histogram equalization and CLAHE to improve low-light images:

```bash
# Process directory of PNG images
python lowlight/lowlight.py <directory>
```
- Applies standard histogram equalization
- Applies CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Generates comparison visualizations

**Output**: Processed images in `lowlight/output/<image_name>/`:
- `*_original_gray.png` - Grayscale original
- `*_equalized.png` - Histogram equalized
- `*_clahe.png` - CLAHE enhanced
- `*_comparison.png` - Side-by-side comparison

Corresponding analysis is hard coded to look for `ECE253/lowlight/output` (i.e., `output` exists in `lowlight` subdirectory). You can either change this path in the `.ipynb` or use the same expected path structure.

#### Zero-DCE Method

Apply Zero-DCE deep learning-based enhancement for low-light images:

1. **Copy dataset to Zero-DCE test directory**:
```bash
copy <processed_images> lowlight/Zero-DCE/Zero-DCE_code/data/test_data/
```

2. **Run Zero-DCE test**:
```bash
python lowlight/Zero-DCE/Zero-DCE_code/lowlight_test.py
```

Corresponding analysis is hard coded to look for `ECE253/lowlight/Zero-DCE/Zero-DCE_code/data/result/dark` (i.e., `dark` is the directory to name the PNG files). You can either change this path in the `.ipynb` or use the same expected path structure.

**Output**: Enhanced images in `lowlight/Zero-DCE/Zero-DCE_code/data/result/dark/`

---

### 2. Glare Detection/Removal

`glare.ipynb`
- Applies classical BM3D denoising to reduce assumed Gaussian noise
- Evaluates a hybrid BM3D + DnCNN residual denoiser
- Compares denoising performance using PSNR, high-frequency energy, and qualitative inspection

To **run**, open the notebook and execute cells with your input image.

---

### 3. Denoise

`denoise.ipynb`
- Detects glare in images using HSV thresholding
- Removes glare using inpainting techniques
- Applies Multi-Scale Retinex (MSR) for additional enhancement

To **run**, open the notebook and execute cells with your input image.

---

### 4. Blur Removal

**Main Function**  

`motionBlur.ipynb`
- Perform Blind RL deconvolution with a 128×128 pixel grid.
- Remove motion blur and out-of-focus blur.
- Suppress the introduced ring artifacts using total variation smoothing.  

**Evaluation** (`evaluation/evaluation.ipynb`):
- Calculate the Tenengrad, Laplacian variance, and frequency-domain metrics.
- Calculate the improvement for individual subjects.

To **run**, open the notebook and execute cells with your input image.

---

### 5. Analysis & Evaluation

**Lowlight Analysis** (`lowlight/analysis.ipynb`):
- Computes and compares cumulative distribution functions (CDF) of pixel intensities
- Analyzes dataset-average CDFs for original, CLAHE, and Zero-DCE enhanced images
- Generates overlay plot to visualize differences in pixel intensity distributions

**Evaluation** (`evaluation/evaluation.ipynb`):
- Calculates image quality metrics (mean, std, contrast, dynamic range)
- Generates histogram comparisons
- Creates difference maps between original and enhanced images

To **run**, open notebooks in Jupyter or VS Code and execute cells sequentially

---

### 6. Daphnia Dataset

`Daphnia_Counter1-5/`

Roboflow-exported dataset in COCO format with:
- 128 annotated images
- Train/test/valid splits
- `_annotations.coco.json` files in each split

---

## Workflow Example

Complete processing pipeline for low-light enhancement:

1. Download and unzip dataset from [Google Drive link](https://drive.google.com/file/d/16f5vKlTksrY68vdscSIL6Uj8a39R3CHN/view?usp=sharing) into the repository root (please sign in with UCSD credentials)
2. Run CLAHE enhancement: `python lowlight/lowlight.py <dataset_directory>`
3. Copy processed images to Zero-DCE: `copy lowlight/output/* lowlight/Zero-DCE/Zero-DCE_code/data/test_data/`
4. Run Zero-DCE enhancement: `python lowlight/Zero-DCE/Zero-DCE_code/lowlight_test.py`
5. Analyze and compare results using `lowlight/analysis.ipynb` and `evaluation/evaluation.ipynb`
