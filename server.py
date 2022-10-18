from gevent.pywsgi import WSGIServer
from index import app
print("MisatoAPI Running...")
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()