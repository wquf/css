import os
import sys
import time
import retry
import flask
import random
import webview
import threading

first = True
window = None
previous = None
file = os.path.abspath(sys.argv[1])

def get():
    with open(file, 'r', encoding='UTF-8') as source:
        content = source.read()
    source.close()
    return content

def update():
    global previous
    while 1:
        if not window and first:
            continue
        elif not window and not first:
            break
        content = get()
        if previous != content:
            previous = content
            window.evaluate_js('window.location.reload()')
        time.sleep(0.1)
    return sys.exit(0)
        
@retry.retry()
def deploy():
    def process():
        global app
        global port
        port = random.randint(8000, 65535)
        
        app = flask.Flask(__name__)
        @app.route('/')
        def _():
            return get()
        return app.run('0.0.0.0', port=port)
    thread = threading.Thread(target=process, daemon=True)
    return thread.start()

deploy() 
window = webview.create_window('HTML Previewer', url=f'http://localhost:{port}')
def closed():
    global window, first
    window = None
    first = False
    return None
window.events.closed += closed
webview.start(func=update)
