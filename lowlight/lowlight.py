import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import sys


def read_image(image_path):
    path = Path(image_path)

    if path.suffix.lower() != ".png":
        raise ValueError(f"Error: {image_path} is not a .png image")

    img = cv2.imread(str(path))
    if img is None:
        raise ValueError(f"Error: Failed to read image {image_path}")

    return img

# apply HE and CLAHE 
def apply_histogram_equalization(image_path, output_dir="output"):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    img = read_image(image_path)  # will also error if not .png
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    base_name = Path(image_path).stem

    image_output_dir = output_dir / base_name
    image_output_dir.mkdir(exist_ok=True)

    # std histogram equalization
    equalized = cv2.equalizeHist(gray)

    # CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_applied = clahe.apply(gray)

    # Save processed images in the image-specific subdirectory
    cv2.imwrite(str(image_output_dir / f"{base_name}_original_gray.png"), gray)
    cv2.imwrite(str(image_output_dir / f"{base_name}_equalized.png"), equalized)
    cv2.imwrite(str(image_output_dir / f"{base_name}_clahe.png"), clahe_applied)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # original img
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original Color")
    axes[0, 0].axis("off")

    # grayscale
    axes[0, 1].imshow(gray, cmap="gray")
    axes[0, 1].set_title("Original Grayscale")
    axes[0, 1].axis("off")

    # std equalization
    axes[1, 0].imshow(equalized, cmap="gray")
    axes[1, 0].set_title("Standard Histogram Equalization")
    axes[1, 0].axis("off")

    # CLAHE
    axes[1, 1].imshow(clahe_applied, cmap="gray")
    axes[1, 1].set_title("CLAHE")
    axes[1, 1].axis("off")

    plt.tight_layout()
    plt.savefig(
        str(image_output_dir / f"{base_name}_comparison.png"),
        dpi=150,
        bbox_inches="tight",
    )
    plt.close()

    print(f"Processed {image_path}")
    print(f"    Saved results to {image_output_dir}/")

    return equalized, clahe_applied


# process directory of images, check if png (not raw, etc.)
def batch_process_images(input_dir, output_dir="output"):
    input_dir = Path(input_dir)

    if not input_dir.is_dir():
        raise ValueError(f"{input_dir} is not a valid directory")

    all_entries = list(input_dir.iterdir())
    non_png_files = [
        p for p in all_entries
        if p.is_file() and p.suffix.lower() != ".png"
    ]

    if non_png_files:
        names = ", ".join(p.name for p in non_png_files)
        raise ValueError(
            f"Non-PNG files detected in {input_dir}: {names}. "
            "Convert or remove them before processing."
        )

    image_files = list(input_dir.glob("*.png"))

    if not image_files:
        raise ValueError(f"No .png images found in {input_dir}")

    print(f"Found {len(image_files)} PNG images")
    print("=" * 60)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    for img_path in image_files:
        apply_histogram_equalization(img_path, output_dir)
        print()

    print("=" * 60)
    print(f"Results saved to {output_dir}/")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])

        if path.is_dir():
            print(f"\nProcessing all PNG images in directory: {path}")
            print()
            batch_process_images(path)

        else:
            raise ValueError(f"{path} is not a valid file or directory")
    else:
        print("\nUsage:")
        print("  python lowlight.py <image_file.png>")
        print("  python lowlight.py <directory>")
