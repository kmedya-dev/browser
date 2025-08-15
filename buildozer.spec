[app]
title = WebView App
package.name = webview_app
package.domain = org.example
source.dir = .
version = 0.1
requirements = python3,kivy,webview-android,openssl,hostpython3,android
orientation = portrait
fullscreen = 0
android.api = 34
android.build_tools_version = 34.0.0
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.manifest.intent_filters = intent_filters.xml
android.permissions = INTERNET
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0

[buildozer]
log_level = 2
warn_on_root = 1
