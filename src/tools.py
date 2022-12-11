from datetime import datetime
from main import html_root


def favicon(handler):
    with open(html_root+'/favicon.ico', 'rb') as ico:
        handler.send_response(200)
        handler.send_header('Content-Type', 'image/x-icon;')
        handler.end_headers()
        handler.wfile.write(ico.read())
        return handler


def capture_error(handler):
    with open(html_root+'/capture_error.html', 'rb') as html:
        handler.send_response(500)
        handler.send_header('Content-Type', 'text/html; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(html.read())
        return handler


def logger(msg):
    print(datetime.now().strftime("[%Y/%m/%d %H:%M:%S]"), msg)



