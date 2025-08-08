# WebView App

A minimal, modern, cross-platform WebView application built with Kivy and Python. This project is designed to be developed in Termux and built automatically via GitHub Actions.

## ✨ Features

- **Cross-Platform:** Runs on Android (via `pyjnius`) and Desktop (Linux/macOS via `pywebview`).
- **Smart Address Bar:** Functions as both a URL navigator and a search bar.
- **Acts as a Browser:** Registers with the Android OS to open `http`/`httpshttps` links from other apps.
- **In-App Console:** A built-in console displays `console.log` messages from the WebView, available on all platforms.
- **Native Android Debugging:** Forwards all console messages to `logcat` for powerful, PC-free inspection.
- **Live-Reload Server:** Includes a built-in web server and file watcher for rapid offline-first web development.
- **CI/CD Ready:** A pre-configured GitHub Actions workflow automatically builds a debug APK on every push.
- **Bookmark Manager:** Save, view, and load your favorite URLs.

## 🛠️ Tech Stack

- **UI Framework:** [Kivy](https://kivy.org/)
- **Android Bridge:** [Pyjnius](https://pyjnius.readthedocs.io/)
- **Desktop WebView:** [pywebview](https://pywebview.flowrl.com/)
- **File Watching:** [Watchdog](https://python-watchdog.readthedocs.io/)
- **Build System:** [Buildozer](https://buildozer.readthedocs.io/)

## 🚀 Getting Started

### Local Development (Offline Web Project)

This project includes a live-reload server for developing the web-based parts of your app.

1.  Run the application:
    ```bash
    python main.py
    ```
2.  Click the **"Live"** button. This starts a server for the `local_web_project/` directory.
3.  Edit any file inside `local_web_project/` (e.g., `index.html`, `style.css`).
4.  The WebView will automatically reload to show your changes.

### Building the APK (CI/CD)

This project is configured to build a debug APK automatically using GitHub Actions.

1.  **Commit and Push:** Push your code to the `main` branch of your GitHub repository.
    ```bash
    git add .
    git commit -m "Your changes"
    git push origin main
    ```
2.  **Check Actions:** Go to the "Actions" tab in your GitHub repository. A new workflow run will be in progress.
3.  **Download Artifacts:** Once the build is complete, you can download two artifacts:
    -   `webview-app-debug-apk`: Contains the installable `.apk` file.
    -   `buildozer-log`: Contains the complete build log, essential for debugging any failures.

---

## 📜 License

**The MIT License (MIT)**

Copyright (c) 2025 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
