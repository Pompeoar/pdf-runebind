# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Install system dependencies required by Marker
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils \
    tesseract-ocr \
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

# Upgrade pip and install marker-pdf
RUN pip install --upgrade pip setuptools wheel && \
    pip install marker-pdf

# Set working directory with proper ownership
WORKDIR /workspace

# Ensure the vscode user owns the workspace directory
RUN chown -R $USERNAME:$USERNAME /workspace

# Switch to non-root user
USER $USERNAME

# Set Python path
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
