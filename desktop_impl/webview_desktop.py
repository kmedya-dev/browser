import webview
from shared.webview_bridge import WebViewBridge
from shared.js_bridge import CONSOLE_OVERRIDE_JS
from kivy.clock import Clock

class DesktopWebView(WebViewBridge):
    def __init__(self, log_callback=None):
        self.window = None
        self.log_callback = log_callback

    def create_webview(self, url, **kwargs):
        # Expose a Python class to the JS environment
        self.api = self.Api(self.log_callback)
        self.window = webview.create_window('WebView App', url, js_api=self.api, **kwargs)
        self.window.events.loaded += self.on_page_load
        return self.window

    def on_page_load(self):
        # Inject the console override script on every page load
        self.evaluate_js(CONSOLE_OVERRIDE_JS)

    def set_url(self, url):
        if self.window:
            self.window.load_url(url)

    def evaluate_js(self, js_code):
        if self.window:
            self.window.evaluate_js(js_code)

    def toggle_theme(self, theme_mode):
        print(f"Theme change to {theme_mode} requested. Desktop follows OS.")

    def set_language(self, lang_code):
        js_code = f"document.documentElement.lang = '{lang_code}';"
        self.evaluate_js(js_code)

    # --- API class exposed to JavaScript ---
    class Api:
        def __init__(self, log_callback):
            self.log_callback = log_callback

        def log(self, message):
            if self.log_callback:
                # No need for Clock.schedule_once on desktop, but good practice
                Clock.schedule_once(lambda dt: self.log_callback(f"JS-CONSOLE: {message}"))