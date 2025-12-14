# ECE253 Image Processing Project

Scripting and automating image processing techniques on photos of Daphnia (D. magna).

## Requirements

Install required Python packages:
```bash
pip install opencv-python numpy matplotlib pandas rawpy imageio scikit-image
```

## Usage

### 1. Image Format Conversion (ORF -> PNG)

Convert Olympus ORF raw files to PNG format:

```bash
# Single file
python util/orf2png.py <file.orf> [output_dir]

# Batch convert directory
python util/orf2png.py <directory> [output_dir]
```

**Output**: PNG files in `converted_png/` (or specified directory)

---

### 2. Low-Light Enhancement

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

---

### 3. Analysis & Evaluation

**Lowlight Analysis** (`lowlight/analysis.ipynb`):
- Compares CLAHE vs Zero-DCE enhancement methods
- Calculates median intensity and CDF metrics
- Generates quantitative comparisons

**Evaluation** (`evaluation/evaluation.ipynb`):
- Calculates image quality metrics (mean, std, contrast, dynamic range)
- Generates histogram comparisons
- Creates difference maps between original and enhanced images

To **run**, open notebooks in Jupyter or VS Code and execute cells sequentially

---

### 4. Glare Detection/Removal

`glare.ipynb`
- Applies classical BM3D denoising to reduce assumed Gaussian noise
- Evaluates a hybrid BM3D + DnCNN residual denoiser
- Compares denoising performance using PSNR, high-frequency energy, and qualitative inspection

To **run**, open the notebook and execute cells with your input image.

---

### 5. Denoise

`denoise.ipynb`
- Detects glare in images using HSV thresholding
- Removes glare using inpainting techniques
- Applies Multi-Scale Retinex (MSR) for additional enhancement

To **run**, open the notebook and execute cells with your input image.

---

### 6. Zero-DCE

Here is the [link](https://github.com/Li-Chongyi/Zero-DCE) for the actual repository. The one here has some minor changes and added files for our usage.

`lowlight/Zero-DCE-master/`

**Output**: Processed images in `lowlight\Zero-DCE-master\Zero-DCE_code\data\result\dark`
- just a subset of images, primarily the ones that looked dark and worse lighting conditions
---

### 7. Daphnia Dataset

`Daphnia_Counter1-5/`

Roboflow-exported dataset in COCO format with:
- 128 annotated images
- Train/test/valid splits
- `_annotations.coco.json` files in each split

---

## Workflow Example

Typical processing pipeline:

1. Convert raw camera files: `python util/orf2png.py original/`
2. Enhance low-light images: `python lowlight/lowlight.py converted_png/`
3. Analyze results using `lowlight/analysis.ipynb`
4. Evaluate quality using `evaluation/evaluation.ipynb`
