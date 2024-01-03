from http.server import HTTPServer, BaseHTTPRequestHandler
from aqt import pyqtSignal, QThread, mw
from .open_card import openBrowseLink

# handle SIGPIPE on macOS
try:
    from signal import signal, SIGPIPE, SIG_IGN
    signal(SIGPIPE,SIG_IGN)
# error gets raised on Windows, nbd
except ImportError:
    pass

class SignalThread(QThread):
    qid_set_signal = pyqtSignal(str)
    
    def set_qid(self, qid):
        self.qid = qid

    def run(self):
        self.qid_set_signal.emit(self.qid)

def do_the_thing(qid):
    config = mw.addonManager.getConfig(__name__)
    openBrowseLink(f"tag:#AK_Step{config['step']}_v{config['AnKing_version']}::#UWorld::*{qid}")

signal_thread = SignalThread()
signal_thread.qid_set_signal.connect(do_the_thing)

class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        signal_thread.set_qid(self.path[1:])
        signal_thread.start()

    def log_message(self, format: str, *args) -> None:
        return
    
    def handle_one_request(self) -> None:
        try:
            super().handle_one_request()
        # gets raised when button is clicked multiple times in rapid succession,
        # or when the button is clicked after a long time
        except ConnectionAbortedError:
            pass

httpd = HTTPServer(('localhost', 8088), MyHandler)

def start_server():
    httpd.serve_forever()

from threading import Thread
thread = Thread(target=start_server, daemon=True, name="uworld_connect")
thread.start()