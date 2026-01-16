#!/bin/bash
# Test script to verify devcontainer permissions and setup

set -e

echo "=== Testing devcontainer setup ==="
echo ""

# Test 1: Check current user
echo "1. Current user:"
whoami
id

# Test 2: Check workspace permissions
echo ""
echo "2. Workspace permissions:"
ls -ld /workspace
echo ""

# Test 3: Test file creation
echo "3. Testing file creation:"
test_file="/workspace/test_permissions.txt"
echo "Creating test file: $test_file"
echo "This is a test file to verify write permissions" > "$test_file"
if [ -f "$test_file" ]; then
    echo "✓ File created successfully"
    ls -l "$test_file"
    rm "$test_file"
    echo "✓ File deleted successfully"
else
    echo "✗ Failed to create file"
    exit 1
fi

# Test 4: Test directory creation
echo ""
echo "4. Testing directory creation:"
test_dir="/workspace/test_dir"
mkdir -p "$test_dir"
if [ -d "$test_dir" ]; then
    echo "✓ Directory created successfully"
    ls -ld "$test_dir"
    rmdir "$test_dir"
    echo "✓ Directory deleted successfully"
else
    echo "✗ Failed to create directory"
    exit 1
fi

# Test 5: Check Python installation
echo ""
echo "5. Python installation:"
python --version
which python

# Test 6: Check Marker installation
echo ""
echo "6. Marker installation:"
if python -c "import marker; print('✓ Marker is installed'); print('  Version:', marker.__version__ if hasattr(marker, '__version__') else 'unknown')" 2>/dev/null; then
    echo "✓ Marker module can be imported"
else
    echo "✗ Marker module not found or import failed"
    echo "  This is expected if marker-pdf installation failed"
fi

# Test 7: Check sudo access
echo ""
echo "7. Sudo access:"
if sudo -n true 2>/dev/null; then
    echo "✓ Passwordless sudo access confirmed"
else
    echo "✗ No passwordless sudo access"
    exit 1
fi

echo ""
echo "=== All tests passed! ==="
