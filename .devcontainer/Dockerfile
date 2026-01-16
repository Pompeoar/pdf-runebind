# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Install system dependencies required by Marker
# Note: libgl1-mesa-glx was replaced by libgl1 in newer Debian versions
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user 'vscode' with sudo privileges
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set up Python environment
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Upgrade pip and install marker-pdf with pinned compatible versions
# Note: This will also install PyTorch (~2GB download)
# transformers must be <4.42 for surya-ocr compatibility (avoids SDPA error)
RUN pip install --upgrade pip setuptools wheel && \
    pip install "marker-pdf>=0.2.0,<0.3" "surya-ocr>=0.4.0,<0.6" "transformers>=4.41.0,<4.42"

# Create directories for model cache with proper ownership
RUN mkdir -p /home/$USERNAME/.cache/huggingface && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME/.cache

# Set working directory with proper ownership
WORKDIR /workspace

# Ensure the vscode user owns the workspace directory
RUN chown -R $USERNAME:$USERNAME /workspace

# Switch to non-root user
USER $USERNAME

# Set Python path
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
