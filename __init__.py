from http.server import HTTPServer, BaseHTTPRequestHandler
from aqt import pyqtSignal, QThread
from .open_card import openBrowseLink


class SignalThread(QThread):
    qid_set_signal = pyqtSignal(str)
    
    def set_qid(self, qid):
        self.qid = qid

    def run(self):
        self.qid_set_signal.emit(self.qid)

def do_the_thing(qid):
    openBrowseLink(f"tag:#AK_Step2_v*::#UWorld::*{qid}")

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
httpd = HTTPServer(('localhost', 8088), MyHandler)

def start_server():
    httpd.serve_forever()

from threading import Thread
thread = Thread(target=start_server, daemon=True, name="uworld_connect")
thread.start()