from abc import ABC, abstractmethod

class WebViewBridge(ABC):
    @abstractmethod
    def create_webview(self, url, **kwargs):
        pass

    @abstractmethod
    def set_url(self, url):
        pass

    @abstractmethod
    def evaluate_js(self, js_code):
        pass

    @abstractmethod
    def toggle_theme(self, theme_mode):
        pass # 'light', 'dark', 'system'

    @abstractmethod
    def set_language(self, lang_code):
        pass # 'en', 'bn'
