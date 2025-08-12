#!/bin/bash
set -e  # exit on error

echo "=== Setting up environment ==="

# Define Android SDK home path (same as in workflow)
export ANDROID_HOME="$HOME/.buildozer/android/platform/android-sdk"
export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"

mkdir -p "$ANDROID_HOME"

echo "=== Installing Android command line tools ==="
if [ ! -d "$ANDROID_HOME/cmdline-tools/latest" ]; then
  wget -q "https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip" -O /tmp/cmdline-tools.zip
  unzip -q /tmp/cmdline-tools.zip -d "$ANDROID_HOME/cmdline-tools"
  mv "$ANDROID_HOME/cmdline-tools/cmdline-tools" "$ANDROID_HOME/cmdline-tools/latest"
else
  echo "Android command line tools already installed."
fi

mkdir -p "$ANDROID_HOME/tools/bin"
ln -sf "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" "$ANDROID_HOME/tools/bin/sdkmanager"

echo "=== Accepting Android SDK licenses ==="
yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_HOME" --licenses

echo "=== Installing required SDK packages ==="
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_HOME" \
  "build-tools;35.0.0" \
  "platforms;android-35" \
  "platform-tools" \
  "ndk;25.1.8937393"

echo "=== Installing Python dependencies ==="
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "=== Installing system packages from prerequisites.txt ==="
if [ -f prerequisites.txt ]; then
  sudo apt-get update
  sudo apt-get install -y $(grep -vE '^\s*#' prerequisites.txt | tr '\n' ' ')
fi

echo "=== Cleaning previous build (optional) ==="
rm -rf .buildozer

echo "=== Setup completed ==="
