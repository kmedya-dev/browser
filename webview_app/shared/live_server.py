import http.server
import socketserver
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LiveServer:
    def __init__(self, path, reload_callback, host="127.0.0.1", port=8000):
        self.path = path
        self.reload_callback = reload_callback
        self.host = host
        self.port = port
        self.server_thread = None
        self.observer_thread = None

    def start(self):
        if self.server_thread and self.server_thread.is_alive():
            return # Already running

        # --- Start HTTP Server ---
        handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args, directory=self.path, **kwargs)
        self.httpd = socketserver.TCPServer((self.host, self.port), handler)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        # --- Start Watchdog Observer ---
        event_handler = self.ChangeHandler(self.reload_callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

        print(f"Live server started at http://{self.host}:{self.port}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print("Live server stopped.")

    class ChangeHandler(FileSystemEventHandler):
        def __init__(self, reload_callback):
            self.reload_callback = reload_callback

        def on_any_event(self, event):
            if event.is_directory or event.event_type not in ['modified', 'created', 'deleted']:
                return
            print(f"File changed: {event.src_path}, triggering reload.")
            self.reload_callback()
