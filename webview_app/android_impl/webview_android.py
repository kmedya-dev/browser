from jnius import autoclass, PythonJavaClass, java_method
from kivy.clock import Clock
from shared.webview_bridge import WebViewBridge
from shared.js_bridge import CONSOLE_OVERRIDE_JS # <-- Import the shared JS

# Autoclass common Android classes
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebChromeClient = autoclass('android.webkit.WebChromeClient')
ConsoleMessage = autoclass('android.webkit.ConsoleMessage')
View = autoclass('android.view.View')

# --- Logcat Bridge: Python class exposed to JavaScript for custom actions ---
class LogcatBridge(PythonJavaClass):
    __javainterfaces__ = ['org/example/webview_app/LogcatBridge']
    __javacontext__ = 'app'

    def __init__(self, log_callback=None):
        super().__init__()
        self.log_callback = log_callback

    @java_method('(Ljava/lang/String;)V')
    def log(self, message):
        # This is now called by our universal JS bridge
        log_msg = f"JS-CONSOLE: {message}"
        if self.log_callback:
            Clock.schedule_once(lambda dt: self.log_callback(log_msg))

# --- Custom WebChromeClient to capture console.log for NATIVE logcat ---
class CustomWebChromeClient(WebChromeClient):
    # This remains for native inspection without a PC (logcat)
    @java_method('(Landroid/webkit/ConsoleMessage;)Z')
    def onConsoleMessage(self, consoleMessage):
        message = consoleMessage.message()
        source_id = consoleMessage.sourceId()
        line_number = consoleMessage.lineNumber()
        print(f"NATIVE-LOGCAT ({source_id}:{line_number}): {message}")
        return True

class AndroidWebView(WebViewBridge):
    def __init__(self, activity, log_callback=None):
        self.activity = activity
        self.webview = None
        self.log_callback = log_callback

    def create_webview(self, url, **kwargs):
        WebView.setWebContentsDebuggingEnabled(True)
        self.webview = WebView(self.activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)

        self.logcat_bridge = LogcatBridge(log_callback=self.log_callback)
        self.webview.addJavascriptInterface(self.logcat_bridge, "LogcatBridge")
        self.webview.setWebViewClient(self._create_webview_client())
        self.webview.setWebChromeClient(CustomWebChromeClient())
        
        self.set_url(url)
        return self.webview

    def set_url(self, url):
        if self.webview:
            self.webview.loadUrl(url)

    def evaluate_js(self, js_code):
        if self.webview:
            self.webview.evaluateJavascript(js_code, None)

    def _create_webview_client(self):
        class CustomWebViewClient(WebViewClient):
            def onPageFinished(self, view, url):
                # Inject the universal console override script
                view.evaluateJavascript(CONSOLE_OVERRIDE_JS, None)
                super().onPageFinished(view, url)
        return CustomWebViewClient()

    def toggle_theme(self, theme_mode):
        print(f"Theme change to {theme_mode} requested. Android follows system.")

    def set_language(self, lang_code):
        js_code = f"document.documentElement.lang = '{lang_code}';"
        self.evaluate_js(js_code)