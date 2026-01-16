# Quick Start Guide

## Convert a Single PDF

1. Drop your PDF into the `input/` folder
2. Run:

```bash
python convert_pdf.py input/your_file.pdf
```

Output goes to `./output/your_file.md`

## Convert a Folder of PDFs

```bash
python batch_convert.py input/ output/
```

## Common Options

| Task | Command |
|------|---------|
| Custom output folder | `python convert_pdf.py file.pdf ./my_folder` |
| Preview batch (no conversion) | `python batch_convert.py /pdfs ./output --dry-run` |
| Keep folder structure | `python batch_convert.py /pdfs ./output --preserve-structure` |

## First Time Setup (Devcontainer)

1. Open in VS Code
2. Click **"Reopen in Container"** when prompted
3. Wait for build to complete (downloads ~2GB of models on first run)

## Mount Your PDFs

Edit `.devcontainer/devcontainer.json`:

```jsonc
"mounts": [
    "source=/path/to/your/PDFs,target=/pdfs,type=bind,consistency=cached"
]
```

Then rebuild the container.
