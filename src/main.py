import threading
import cv2
from urllib.parse import urlparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

import tools
from tools import logger

html_root = "/usr/UVC-Capture/src/www"  # HTMLが格納されているディレクトリ
server_config = ('', 80)

uvc_ok = False


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=html_root, **kwargs)

    def log_message(self, format, *args):
        pass  # ログ出力を無視

    def do_GET(self):
        global uvc_ok
        logger('GET path = {}'.format(self.path))
        parsed_path = urlparse(self.path)

        # ファビコン要求されたらファビコン返す
        if parsed_path.path == '/favicon.ico':
            tools.favicon(self)
            return

        if not uvc_ok:
            tools.uvc_device_error(self)
            return

        # キャプチャ画像要求
        if parsed_path.path == '/capture.jpg':
            # UVCデバイスから画像を取得
            ret, frame = cap.read()

            # 取得に失敗したらエラー返す
            if not ret:
                tools.capture_error(self)
                return

            # jpg化したバイナリ
            content = cv2.imencode(".jpg", frame)[1]

            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(content)
            return

        # ルート要求はindex.html
        elif parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(html_root+'/index.html', 'rb') as f:
                self.wfile.write(f.read())
            return

        # ルート要求はindex.html
        elif parsed_path.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-Type', 'text/css; charset=utf-8')
            self.end_headers()
            with open(html_root+'/style.css', 'rb') as f:
                self.wfile.write(f.read())
            return

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'plane/text; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'HTTP State 404')
            return


def begin_dummy_server():
    httpd = HTTPServer(server_config, Handler)
    print(f'HTTPServer began -> http://192.168.239.183:{server_config[1]}/')
#    httpd.serve_forever()
    server_thread = threading.Thread(target=httpd.serve_forever)  # スレッドで動かす
#    server_thread.daemon = True
    server_thread.start()


def init():
    global uvc_ok
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        uvc_ok = True
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    else:
        logger('Cannot open the UVC device.')
    return cap


if __name__ == "__main__":
    cap = init()
    begin_dummy_server()
    logger("Server start.")
