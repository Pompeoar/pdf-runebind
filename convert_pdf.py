"""
PDF to Agent-Friendly Format Converter

This module provides functionality to convert PDF files to markdown format
using the Marker library, making them more suitable for AI agents to process.
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Dict, List

# Configure environment for large PDF processing
# No page limits - process entire documents
os.environ.setdefault("MARKER_MAX_PAGES", "")
os.environ.setdefault("MARKER_PAGINATE_OUTPUT", "false")
# Increase recursion limit for complex PDFs
sys.setrecursionlimit(10000)


def convert_pdf_to_markdown(pdf_path: str, output_dir: str = "./output") -> Tuple[str, str]:
    """
    Convert a PDF file to markdown format using Marker.
    
    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory to save the output markdown file (default: ./output)
        
    Returns:
        Tuple containing (output_path, markdown_content)
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        PermissionError: If unable to create output directory or file
    """
    try:
        from marker.convert import convert_single_pdf
        from marker.models import load_all_models
    except ImportError:
        print("Error: marker-pdf is not installed. Please install it with: pip install marker-pdf")
        sys.exit(1)
    
    # Validate input file - check input/ folder if not found directly
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        # Try looking in the input/ folder
        input_folder_path = Path("input") / pdf_file.name
        if input_folder_path.exists():
            pdf_file = input_folder_path
        else:
            raise FileNotFoundError(f"PDF file not found: {pdf_file} (also checked input/ folder)")
    
    # Create output directory if it doesn't exist
    output_path_dir = Path(output_dir)
    try:
        output_path_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"Unable to create output directory: {output_path_dir}")
    
    print(f"Loading Marker models...")
    models = load_all_models()
    
    print(f"Converting {pdf_file.name} to markdown...")
    # Note: images and metadata are returned but not currently used
    # They could be used in future enhancements for image extraction or metadata processing
    full_text, images, metadata = convert_single_pdf(
        str(pdf_file),
        models
    )
    
    # Generate output filename
    output_filename = pdf_file.stem + ".md"
    output_path = output_path_dir / output_filename
    
    # Handle filename conflicts by adding a number suffix
    counter = 1
    while output_path.exists():
        output_filename = f"{pdf_file.stem}_{counter}.md"
        output_path = output_path_dir / output_filename
        counter += 1
    
    # Write markdown content to file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Successfully converted PDF to: {output_path}")
    except PermissionError:
        raise PermissionError(f"Unable to write to output file: {output_path}")
    
    return str(output_path), full_text


def main():
    """Main entry point for the PDF converter."""
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf.py <pdf_file> [output_directory]")
        print("Example: python convert_pdf.py document.pdf ./converted")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    try:
        output_path, _ = convert_pdf_to_markdown(pdf_file, output_dir)
        print(f"\n✓ Conversion complete!")
        print(f"  Output: {output_path}")
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
