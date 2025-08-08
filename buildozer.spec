[app]
title = WebView App
package.name = webview_app
package.domain = org.example
source.dir = .
version = 0.1
requirements = python3,kivy,pyjnius==1.6.1,webview-android,openssl,hostpython3,android
orientation = portrait
fullscreen = 0
android.api = 33
android.build_tools_version = 33.0.2
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.manifest.intent_filters = intent_filters.xml

[buildozer]
log_level = 2
warn_on_root = 1
