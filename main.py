import time
import retry
import flask
import random
import webview
import threading

previous = '<body><strong>파일을 선택해주세요!</strong></body>'
closed = False

on_closed = lambda: globals().update({'closed': True})

def update():
    global previous
    file = window.create_file_dialog(file_types=['HyperText Markup Language (*.html)'])[0]
    while 1:
        if closed:
            break

        with open(file, 'r', encoding='UTF-8') as source:
            content = source.read()
        source.close()
            
        if previous != content:
            previous = content
            window.evaluate_js('window.location.reload()')

        time.sleep(0.5)
    return exit(0)
        
@retry.retry()
def deploy():
    global port
    app = flask.Flask(__name__)
        
    index = app.route('/')
    index(lambda: previous)
        
    port = random.randint(8000, 19000)
    return app.run('0.0.0.0', port)

thread = threading.Thread(target=deploy, daemon=True)
thread.start()

window = webview.create_window('Live HTML Viewer', url=f'http://localhost:{port}')
window.events.closed += on_closed

webview.start(update)
