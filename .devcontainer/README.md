# Devcontainer for PDF Runebind

This devcontainer provides a complete development environment for PDF conversion using Python and Marker.

## What's Included

- **Python 3.11**: Latest stable Python version
- **Marker**: Advanced PDF to Markdown conversion tool
- **System Dependencies**: 
  - OCR support (Tesseract)
  - PDF utilities (Poppler)
  - OpenCV dependencies
  - Build tools

## User Permissions

The container runs as a non-root user (`vscode`) with:
- Full sudo privileges (passwordless)
- Read/write access to the workspace
- Ability to create files and directories
- Proper ownership of all workspace files

## Getting Started

1. Open this repository in VS Code
2. When prompted, click "Reopen in Container"
3. VS Code will build and start the devcontainer
4. Once ready, you can start working with PDFs

## Using Marker

Marker is pre-installed and ready to use. Example usage:

```python
from marker.convert import convert_single_pdf
from marker.models import load_all_models

# Load models
models = load_all_models()

# Convert PDF to Markdown
full_text, images, metadata = convert_single_pdf(
    "path/to/your/file.pdf",
    models
)

# Save the converted markdown
with open("output.md", "w") as f:
    f.write(full_text)
```

## File Permissions

The devcontainer is configured to ensure:
- All files created in `/workspace` are owned by the `vscode` user
- New directories can be created without permission issues
- Git operations work seamlessly
- Python package installations can be done in user space

## Troubleshooting

If you encounter permission issues:
- The container automatically runs `chown -R vscode:vscode /workspace` on creation
- You can manually fix permissions with: `sudo chown -R vscode:vscode /workspace`
- User has passwordless sudo access for system-level operations
