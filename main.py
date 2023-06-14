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
current = None
file = sys.argv[1]

def update():
    global previous
    while 1:
        if not window and first:
            continue
        elif not first:
            break

        with open(file, 'r', encoding='UTF-8') as source:
            content = source.read()
        source.close()

        if previous != content:
            previous = content
            window.evaluate_js('window.location.reload()')

        time.sleep(0.5)
    return sys.exit(0)
        
@retry.retry()
def deploy():
    def process():
        global port
        port = random.randint(8000, 19000)

        app = flask.Flask(__name__)
        app.route('/')(lambda: previous)
        return app.run('0.0.0.0', port)
    
    thread = threading.Thread(target=process, daemon=True)
    return thread.start()

deploy() 
window = webview.create_window('Live HTML Viewer', url=f'http://localhost:{port}')
window.events.closed += lambda: globals().update({'window': None, 'first': False})
webview.start(func=update)
