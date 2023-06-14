import sys
import time
import retry
import flask
import random
import webview
import threading

file     = sys.argv[1]
first    = True
window   = None
current  = None
previous = None

def update():
    global previous
    while 1:
        if not window and first:
            continue
        elif not first:
            break

        source = open(file, 'r', encoding='UTF-8')
        content = source.read()
        source.close()
        
        if previous != content:
            previous = content
            window.evaluate_js('window.location.reload()')

        time.sleep(0.5)
    return sys.exit(0)
        
@retry.retry()
def deploy():
    def run():
        global port
        port = random.randint(8000, 19000)

        app = flask.Flask(__name__)
        
        index = app.route('/')
        index(lambda: previous)
        
        return app.run('0.0.0.0', port)
    
    thread = threading.Thread(target=run, daemon=True)
    return thread.start()

deploy() 

window = webview.create_window('Live HTML Viewer', url=f'http://localhost:{port}')
window.events.closed += lambda: globals().update({'window': None, 'first': False})

webview.start(func=update)
