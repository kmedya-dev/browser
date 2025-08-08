import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window
from shared.live_server import LiveServer
import threading
import urllib.parse
import os

# --- Platform-specific WebView loader ---
def get_webview_bridge(log_callback=None):
    if platform == 'android':
        from android_impl.webview_android import AndroidWebView
        from jnius import autoclass
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        return AndroidWebView(activity, log_callback=log_callback)
    else:
        from desktop_impl.webview_desktop import DesktopWebView
        return DesktopWebView(log_callback=log_callback)

class WebViewApp(App):
    def build(self):
        self.store = JsonStore('bookmarks.json')
        self.root_layout = BoxLayout(orientation='vertical')

        # --- URL Input and Controls ---
        self.url_input = TextInput(text='https://www.google.com', multiline=False, size_hint_y=None, height=44)
        self.url_input.bind(on_text_validate=self.load_url)
        
        controls = BoxLayout(size_hint_y=None, height=44)
        go_button = Button(text='Go')
        go_button.bind(on_press=self.load_url)
        
        save_button = Button(text='Save')
        save_button.bind(on_press=self.save_bookmark)
        
        bookmarks_button = Button(text='Bookmarks')
        bookmarks_button.bind(on_press=self.show_bookmarks)

        theme_button = Button(text='Theme')
        theme_button.bind(on_press=self.toggle_theme)
        lang_button = Button(text='Lang')
        lang_button.bind(on_press=self.switch_language)

        live_button = Button(text='Live')
        live_button.bind(on_press=self.toggle_live_server)

        controls.add_widget(go_button)
        controls.add_widget(save_button)
        controls.add_widget(bookmarks_button)
        controls.add_widget(theme_button)
        controls.add_widget(lang_button)
        controls.add_widget(live_button)

        self.root_layout.add_widget(self.url_input)
        self.root_layout.add_widget(controls)

        # --- In-App Console UI ---
        self.log_label = Label(text='Console Logs:\n', size_hint_y=None, markup=True)
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        log_scroll = ScrollView(size_hint=(1, 0.3))
        log_scroll.add_widget(self.log_label)

        # --- WebView Bridge Initialization ---
        self.webview_bridge = get_webview_bridge(log_callback=self.update_log_view)

        # --- Handle Incoming URL Intent ---
        initial_url = self.handle_intent()
        if initial_url:
            self.url_input.text = initial_url
        else:
            initial_url = self.url_input.text

        # --- Create and add the WebView ---
        webview_container = self.setup_webview_container(initial_url)
        self.root_layout.add_widget(webview_container)
        self.root_layout.add_widget(log_scroll)

        self.live_server = None
        self.is_live_mode = False

        # Bind to on_resume to handle intents when app is already running
        Window.bind(on_resume=self.on_app_resume)
        # Make sure to stop the server when the app closes
        Window.bind(on_request_close=self.on_request_close)

        return self.root_layout

    def handle_intent(self):
        if platform != 'android':
            return None
        
        from jnius import autoclass
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        intent = activity.getIntent()
        action = intent.getAction()
        
        if action == "android.intent.action.VIEW":
            url = intent.getDataString()
            if url:
                self.update_log_view(f"[APP] Got URL from intent: {url}")
                return url
        return None

    def on_app_resume(self, *args):
        # Handle intent when app is resumed
        url = self.handle_intent()
        if url:
            self.url_input.text = url
            self.webview_bridge.set_url(url)

    def setup_webview_container(self, initial_url):
        if platform == 'android':
            from kivy.uix.widget import Widget
            from android.runnable import run_on_ui_thread

            container = Widget(size_hint=(1, 0.7))
            @run_on_ui_thread
            def create_android_webview():
                webview_widget = self.webview_bridge.create_webview(initial_url)
                container.add_widget(webview_widget)
            create_android_webview()
            return container
        else:
            label = Label(text='WebView is initializing...\nLogs will appear below.', size_hint=(1, 0.7))
            threading.Thread(target=self.webview_bridge.create_webview, args=(initial_url,)).start()
            return label

    def on_request_close(self, *args):
        if self.live_server:
            self.live_server.stop()
        return True

    def toggle_live_server(self, instance):
        if self.is_live_mode:
            # Turn off live mode
            self.is_live_mode = False
            if self.live_server:
                self.live_server.stop()
            self.update_log_view("[APP] Live server stopped.")
            instance.text = "Live"
        else:
            # Turn on live mode
            self.is_live_mode = True
            project_path = os.path.join(os.path.dirname(__file__), 'local_web_project')
            self.live_server = LiveServer(project_path, reload_callback=self.reload_webview_content)
            self.live_server.start()
            
            url = f"http://{self.live_server.host}:{self.live_server.port}"
            self.url_input.text = url
            self.webview_bridge.set_url(url)
            self.update_log_view(f"[APP] Live server started at {url}")
            instance.text = "Stop"

    def reload_webview_content(self):
        # This needs to be run on the main thread
        Clock.schedule_once(lambda dt: self.webview_bridge.evaluate_js('window.location.reload()'))

    def update_log_view(self, log_message):
        self.log_label.text += f"{log_message}\n"

    def load_url(self, instance):
        text = self.url_input.text.strip()
        
        # Simple check to see if it's a URL or a search term
        # This can be improved, but it's a good start.
        if '.' in text and ' ' not in text:
            url = text
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
        else:
            # It's a search term, so format it for a Google search
            query = urllib.parse.quote_plus(text)
            url = f"https://www.google.com/search?q={query}"

        self.update_log_view(f"[APP] Loading URL: {url}")
        self.webview_bridge.set_url(url)

    def toggle_theme(self, instance):
        current_theme = getattr(self, '_theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.webview_bridge.toggle_theme(new_theme)
        self._theme = new_theme
        self.update_log_view(f"[APP] Theme set to {new_theme}")

    def switch_language(self, instance):
        current_lang = getattr(self, '_lang', 'en')
        new_lang = 'bn' if current_lang == 'en' else 'en'
        self.webview_bridge.set_language(new_lang)
        self._lang = new_lang
        self.update_log_view(f"[APP] Language set to {new_lang}")

    def save_bookmark(self, instance):
        url = self.url_input.text.strip()
        if url:
            self.store.put(url, title=url) # For simplicity, title is the URL
            self.update_log_view(f"[APP] Bookmark saved: {url}")

    def show_bookmarks(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        for url in self.store:
            bookmark_entry = BoxLayout(size_hint_y=None, height=44)
            btn = Button(text=url)
            btn.bind(on_press=lambda x, url=url: self.load_bookmark(url))
            delete_btn = Button(text='X', size_hint_x=0.2)
            delete_btn.bind(on_press=lambda x, url=url: self.delete_bookmark(url))
            bookmark_entry.add_widget(btn)
            bookmark_entry.add_widget(delete_btn)
            popup_layout.add_widget(bookmark_entry)

        popup = Popup(title='Bookmarks', content=popup_layout, size_hint=(0.9, 0.9))
        popup.open()

    def load_bookmark(self, url):
        self.url_input.text = url
        self.load_url(None)

    def delete_bookmark(self, url):
        if self.store.exists(url):
            self.store.delete(url)
            self.update_log_view(f"[APP] Bookmark deleted: {url}")

if __name__ == '__main__':
    WebViewApp().run()