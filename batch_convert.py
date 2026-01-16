#!/usr/bin/env python3
"""
Batch PDF to Markdown Converter

Converts all PDFs in a directory (optionally recursive) to markdown format.
Useful for processing entire collections of sourcebooks at once.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure environment for large PDF processing
# No page limits - process entire documents
os.environ.setdefault("MARKER_MAX_PAGES", "")
os.environ.setdefault("MARKER_PAGINATE_OUTPUT", "false")
# Increase recursion limit for complex PDFs
sys.setrecursionlimit(10000)

# Cache models globally to avoid reloading for each file
_models = None


def get_models():
    """Load models once and cache them."""
    global _models
    if _models is None:
        try:
            from marker.models import load_all_models
            print("Loading Marker models (this may take a minute on first run)...")
            _models = load_all_models()
            print("Models loaded successfully.\n")
        except ImportError:
            print("Error: marker-pdf is not installed.")
            print("Install with: pip install 'marker-pdf>=0.2.0,<1.0'")
            sys.exit(1)
    return _models


def convert_single_file(pdf_path: Path, output_dir: Path, preserve_structure: bool = False, 
                        base_input_dir: Optional[Path] = None) -> Tuple[bool, str, str]:
    """
    Convert a single PDF file to markdown.
    
    Returns:
        Tuple of (success, input_path, output_path_or_error)
    """
    try:
        from marker.convert import convert_single_pdf
        
        models = get_models()
        
        # Determine output path
        if preserve_structure and base_input_dir:
            # Preserve directory structure relative to input base
            relative_path = pdf_path.relative_to(base_input_dir)
            output_subdir = output_dir / relative_path.parent
        else:
            output_subdir = output_dir
        
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        output_filename = pdf_path.stem + ".md"
        output_path = output_subdir / output_filename
        
        # Handle filename conflicts
        counter = 1
        while output_path.exists():
            output_filename = f"{pdf_path.stem}_{counter}.md"
            output_path = output_subdir / output_filename
            counter += 1
        
        # Convert
        full_text, images, metadata = convert_single_pdf(str(pdf_path), models)
        
        # Write output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        return True, str(pdf_path), str(output_path)
        
    except Exception as e:
        return False, str(pdf_path), str(e)


def find_pdfs(input_dir: Path, recursive: bool = True) -> List[Path]:
    """Find all PDF files in the input directory."""
    pattern = "**/*.pdf" if recursive else "*.pdf"
    return list(input_dir.glob(pattern))


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert PDFs to agent-friendly markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all PDFs in a folder
  python batch_convert.py ./my_sourcebooks ./output
  
  # Non-recursive (only top-level PDFs)
  python batch_convert.py ./pdfs ./output --no-recursive
  
  # Preserve directory structure in output
  python batch_convert.py ./pdfs ./output --preserve-structure
        """
    )
    
    parser.add_argument("input_dir", help="Directory containing PDF files")
    parser.add_argument("output_dir", help="Directory for output markdown files")
    parser.add_argument("--no-recursive", action="store_true", 
                        help="Don't search subdirectories for PDFs")
    parser.add_argument("--preserve-structure", action="store_true",
                        help="Preserve directory structure in output")
    parser.add_argument("--dry-run", action="store_true",
                        help="List PDFs that would be converted without converting")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    recursive = not args.no_recursive
    
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    # Find PDFs
    print(f"Searching for PDFs in {input_dir}{'(recursive)' if recursive else ''}...")
    pdf_files = find_pdfs(input_dir, recursive)
    
    if not pdf_files:
        print("No PDF files found.")
        sys.exit(0)
    
    print(f"Found {len(pdf_files)} PDF file(s):\n")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    if args.dry_run:
        print("\n[Dry run - no files converted]")
        sys.exit(0)
    
    print(f"\nConverting to: {output_dir}\n")
    print("-" * 50)
    
    # Convert files
    successful = 0
    failed = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Converting: {pdf_path.name}...", end=" ", flush=True)
        
        success, input_path, result = convert_single_file(
            pdf_path, 
            output_dir, 
            args.preserve_structure,
            input_dir
        )
        
        if success:
            print(f"✓")
            print(f"         -> {result}")
            successful += 1
        else:
            print(f"✗ Error: {result}")
            failed += 1
    
    print("-" * 50)
    print(f"\nComplete! {successful} succeeded, {failed} failed.")
    
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
