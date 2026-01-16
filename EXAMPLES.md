# PDF Runebind Usage Examples

This document provides examples of how to use pdf-runebind to convert PDFs to agent-friendly markdown format.

## Basic Usage

### Command Line Interface

Convert a single PDF file:

```bash
python convert_pdf.py document.pdf
```

This creates a markdown file in the `./output` directory.

### Custom Output Directory

```bash
python convert_pdf.py document.pdf ./my_converted_files
```

### Batch Processing Multiple PDFs

```bash
for pdf in *.pdf; do
    python convert_pdf.py "$pdf"
done
```

## Python API Examples

### Simple Conversion

```python
from convert_pdf import convert_pdf_to_markdown

# Convert a PDF to markdown
output_path, markdown_text = convert_pdf_to_markdown(
    "research_paper.pdf",
    output_dir="./output"
)

print(f"Converted file saved to: {output_path}")
print(f"Content length: {len(markdown_text)} characters")
```

### Processing Multiple Files

```python
import os
from pathlib import Path
from convert_pdf import convert_pdf_to_markdown

# Directory containing PDFs
pdf_dir = Path("./pdfs")
output_dir = Path("./converted")

# Process all PDFs
for pdf_file in pdf_dir.glob("*.pdf"):
    try:
        output_path, content = convert_pdf_to_markdown(
            str(pdf_file),
            output_dir=str(output_dir)
        )
        print(f"✓ Converted: {pdf_file.name} -> {output_path}")
    except Exception as e:
        print(f"✗ Failed to convert {pdf_file.name}: {e}")
```

### Using Markdown Content Directly

```python
from convert_pdf import convert_pdf_to_markdown

# Convert and use the markdown content
_, markdown_content = convert_pdf_to_markdown("document.pdf")

# Example: Count sections
section_count = markdown_content.count('\n## ')
print(f"Document has {section_count} main sections")

# Example: Extract first 500 characters as summary
summary = markdown_content[:500] + "..."
print(f"Summary: {summary}")
```

### Error Handling

```python
from convert_pdf import convert_pdf_to_markdown
import sys

try:
    output_path, content = convert_pdf_to_markdown(
        "important_document.pdf",
        output_dir="./critical_outputs"
    )
    print(f"Success! File at: {output_path}")
except FileNotFoundError as e:
    print(f"PDF file not found: {e}")
    sys.exit(1)
except PermissionError as e:
    print(f"Permission denied: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
```

## Using with AI Agents

The markdown output is optimized for AI agent consumption:

```python
from convert_pdf import convert_pdf_to_markdown

# Convert PDF to agent-friendly format
_, markdown = convert_pdf_to_markdown("legal_document.pdf")

# Example: Send to an AI agent (pseudo-code)
# agent_response = ai_agent.analyze(markdown)
# print(agent_response)

# The markdown preserves:
# - Document structure (headings, sections)
# - Tables (converted to markdown tables)
# - Lists and formatting
# - Text that was extracted via OCR if needed
```

## Tips for Best Results

1. **File Permissions**: Ensure you have read access to the PDF and write access to the output directory
2. **Large Files**: For very large PDFs, the conversion may take several minutes
3. **Image-Heavy PDFs**: PDFs with many images will take longer due to OCR processing
4. **Output Directory**: The output directory will be created automatically if it doesn't exist
5. **Filename**: Output filename matches input filename with `.md` extension

## Troubleshooting

### Permission Errors

If you encounter permission errors:

```bash
# In devcontainer
sudo chown -R vscode:vscode /workspace
```

### Import Errors

If you see "marker-pdf is not installed":

```bash
pip install -r requirements.txt
```

### Memory Issues

For very large PDFs, you may need to increase available memory:

```bash
# Run with more memory allocated
ulimit -v unlimited
python convert_pdf.py large_document.pdf
```
