#!/bin/bash
set -e

FILE="commandlinetools-linux-13114758_latest.zip"

if [ ! -f "$FILE" ]; then
    echo "❌ File '$FILE' not found!"
    exit 1
fi

# Find next tag
LAST_TAG=$(git tag --sort=-v:refname | head -n 1)
if [ -z "$LAST_TAG" ]; then
    NEXT_TAG="v1.0.0"
else
    VERSION_NUM=$(echo "$LAST_TAG" | sed 's/v//')
    IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION_NUM"
    PATCH=$((PATCH + 1))
    NEXT_TAG="v${MAJOR}.${MINOR}.${PATCH}"
fi

echo "📌 Next release tag: $NEXT_TAG"

# Delete old tag if exists
git tag -d "$NEXT_TAG" 2>/dev/null || true
git push origin --delete "$NEXT_TAG" 2>/dev/null || true

# Create & push new tag
git tag "$NEXT_TAG"
git push origin "$NEXT_TAG"

# Progress + Upload
echo "⬆️ Uploading '$FILE' to GitHub Release..."
TMP_FILE=$(mktemp)
pv "$FILE" > "$TMP_FILE"
mv "$TMP_FILE" "$FILE"

# Create release with file
gh release create "$NEXT_TAG" "$FILE" \
  --title "$NEXT_TAG" \
  --notes "Release $NEXT_TAG with Android Command Line Tools"

echo "✅ Release $NEXT_TAG created successfully!"
