# pdf-runebind
Simple tool to convert your PDFs to something more Agent friendly

## Features

- Convert PDF files to Markdown format using [Marker](https://github.com/VikParuchuri/marker)
- Agent-friendly output optimized for AI processing
- Easy-to-use Python API and CLI

## Development Environment

This project includes a complete VS Code devcontainer with:
- Python 3.11
- Marker PDF conversion library (pinned to 0.x API for stability)
- All necessary system dependencies (OCR, PDF utilities)
- Proper user permissions for file operations
- Persistent model cache (avoids re-downloading ~2GB of models)

### Getting Started with Devcontainer

1. Install [Docker](https://www.docker.com/products/docker-desktop) and [VS Code](https://code.visualstudio.com/)
2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Open this repository in VS Code
4. Click "Reopen in Container" when prompted (or use Command Palette: "Dev Containers: Reopen in Container")
5. Wait for the container to build (first time takes a while - downloads PyTorch + models)

### Mounting Your PDF Folders

To access PDFs from your host machine, edit `.devcontainer/devcontainer.json` and uncomment/modify the mounts section:

```jsonc
"mounts": [
    // Example: Mount your PDFs folder
    "source=C:/Users/YourName/Documents/PDFs,target=/pdfs,type=bind,consistency=cached",
    // ... existing cache mount
]
```

Then rebuild the container.

## Usage

### Command Line - Single File

```bash
python convert_pdf.py your_document.pdf
```

This will convert `your_document.pdf` to markdown and save it in the `./output` directory.

You can specify a custom output directory:

```bash
python convert_pdf.py your_document.pdf ./my_output
```

### Command Line - Batch Conversion

For converting entire folders of PDFs (like your sourcebook collection):

```bash
# Convert all PDFs in a folder (recursive)
python batch_convert.py /pdfs ./output

# Preview what would be converted
python batch_convert.py /pdfs ./output --dry-run

# Preserve folder structure in output
python batch_convert.py /pdfs ./output --preserve-structure
```

### Python API

```python
from convert_pdf import convert_pdf_to_markdown

output_path, markdown_content = convert_pdf_to_markdown(
    "document.pdf",
    output_dir="./output"
)
print(f"Converted to: {output_path}")
```

## Requirements

- Python 3.11+
- See `requirements.txt` for Python dependencies
- System dependencies (included in devcontainer):
  - Tesseract OCR
  - Poppler utils
  - OpenCV libraries

## Installation (Outside Devcontainer)

```bash
pip install -r requirements.txt
```

Note: System dependencies must be installed separately. Using the devcontainer is recommended.

## License

MIT License - see LICENSE file for details
