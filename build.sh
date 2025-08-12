#!/bin/bash
set -e  # exit on error

echo "=== Building debug APK ==="
mkdir -p logs
buildozer -v android debug | tee logs/buildozer-output.log

echo "=== Build completed ==="
echo "APK should be in the bin/ directory."