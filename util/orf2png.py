import rawpy
import imageio
import sys
from pathlib import Path


def convert_orf_to_png(orf_path, output_dir="converted_png"):
    orf_path = Path(orf_path)
    
    if orf_path.suffix.lower() != ".orf":
        raise ValueError(f"Error: {orf_path} is not a .orf file")
    
    if not orf_path.exists():
        raise ValueError(f"Error: {orf_path} does not exist")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    try:
        # read raw file
        with rawpy.imread(str(orf_path)) as raw:
            # Process to png, have to be rbg image
            rgb = raw.postprocess(
                gamma = (5,5),
                no_auto_bright = True,
                output_bps = 8,
                use_camera_wb = True,
                output_color=rawpy.ColorSpace.sRGB
            )
        
        # output path/filename
        output_path = output_dir / f"{orf_path.stem}.png"
        
        # save img
        imageio.imwrite(str(output_path), rgb)
        
        print(f"Converted: {orf_path.name} -> {output_path}")
        return output_path
        
    except Exception as e:
        raise ValueError(f"Error converting {orf_path}: {str(e)}")


# func to convert directory of imgs
def batch_convert_orf_to_png(input_dir, output_dir="converted_png"):
    input_dir = Path(input_dir)
    
    if not input_dir.is_dir():
        raise ValueError(f"{input_dir} is not a valid directory")
    
    # find all .orf files
    orf_files = list(input_dir.glob("*.orf")) + list(input_dir.glob("*.ORF"))
    
    if not orf_files:
        raise ValueError(f"No .orf files found in {input_dir}")
    
    print(f"Found {len(orf_files)} .orf files")
    print("=" * 50)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    successful = 0
    failed = []
    
    for orf_path in orf_files:
        try:
            convert_orf_to_png(orf_path, output_dir)
            successful += 1
        except Exception as e:
            print(f"Failed to convert {orf_path.name}: {str(e)}")
            failed.append(orf_path.name)
    
    print("=" * 50)
    print(f"Successfully converted: {successful}/{len(orf_files)}")
    
    if failed:
        print(f"Failed conversions: {len(failed)}")
        for name in failed:
            print(f"  - {name}")
    
    print(f"\nPNG files saved to: {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "converted_png"
        
        if path.is_file():
            if path.suffix.lower() != ".orf":
                raise ValueError(f"{path} is not a .orf file")
            print(f"Converting single .orf file: {path}\n")
            output_path = convert_orf_to_png(path, output_dir)
            print(f"\n Conversion successful!")
            print(f"  Output: {output_path}")
            
        elif path.is_dir():
            print(f"Converting all .orf files in directory: {path}\n")
            batch_convert_orf_to_png(path, output_dir)
            
        else:
            raise ValueError(f"{path} is not a valid file or directory")
    else:
        print("Usage:")
        print("  python orf_to_png_converter.py <file.orf> [output_dir]")
        print("  python orf_to_png_converter.py <directory> [output_dir]")
        print()
        print("Examples:")
        print("  python orf_to_png_converter.py daphnia.orf")
        print("  python orf_to_png_converter.py daphnia.orf my_pngs")
        print("  python orf_to_png_converter.py ./daphnia_raw_images/")
        print("  python orf_to_png_converter.py ./daphnia_raw_images/ converted_images")
        print()
        print("Note: Requires 'rawpy' and 'imageio' packages")
        print("      Install with: pip install rawpy imageio")