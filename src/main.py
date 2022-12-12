import sys
import threading
import cv2
from urllib.parse import urlparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

import tools

html_root = "/usr/UVC-Capture/src/www"  # HTMLが格納されているディレクトリ
server_config = ('', 8081)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=html_root, **kwargs)

    def log_message(self, format, *args):
        pass  # ログ出力を無視

    def do_GET(self):
        tools.logger('GET path = {}'.format(self.path))
        parsed_path = urlparse(self.path)

        # ファビコン要求されたらファビコン返す
        if parsed_path.path == '/favicon.ico':
            tools.favicon(self)
            return

        # キャプチャ画像要求
        if parsed_path.path == '/capture.jpg':
            # UVCデバイスから画像を取得
            ret, frame = cap.read()

            # 取得に失敗したら強制終了
            if not ret:
                sys.exit(-2)

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
#    httpd.serve_forever()
    server_thread = threading.Thread(target=httpd.serve_forever)  # スレッドで動かす
#    server_thread.daemon = True
    server_thread.start()


def init():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    else:
        tools.logger('Cannot open the UVC device.')
        sys.exit(-1)
    return cap


if __name__ == "__main__":
    cap = init()
    begin_dummy_server()
    tools.logger("Server start.")
