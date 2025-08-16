[app]
title = WebView App
package.name = webview_app
package.domain = org.example
source.dir = .
version = 0.1

# Requirements list
requirements = python3,kivy,pyjnius,webview-android,openssl,hostpython3,android
orientation = portrait
fullscreen = 0
android.api = 35
android.build_tools_version = 35.0.0
android.minapi = 24
android.ndk = 28c
android.archs = arm64-v8a, armeabi-v7a
android.manifest.intent_filters = intent_filters.xml
android.permissions = INTERNET
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0
p4a.url = https://github.com/kmedya-dev/python-for-android
p4a.branch = kmedya-dev-patch-2

[buildozer]
log_level = 2
warn_on_root = 1
