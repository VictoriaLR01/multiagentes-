from pyngrok        import ngrok
from http.server    import BaseHTTPRequestHandler, HTTPServer

import json
import logging
import os
'''
Para que el server funcione
crear entorno virtual
python -m venv nombreDelEntorno
nombreDelEntorno\Scripts\activate
pip install mesa
pip install pyngrok
'''

from Estacionamiento import Estacionamiento

# creamos el modelo
numero_de_agentes = 80
model = Estacionamiento(numero_de_agentes)

def features(data, tipo):
    features = []
    if tipo == 'admin':
        feature = {'cajo_vehi' : data[0]['cajo_vehi'],
                   'cajo_disc' : data[0]['cajo_disc'],
                   'cajo_moto' : data[0]['cajo_moto']}
        features.append(feature)
    elif tipo == 'cajones':
        for elem in data:
            feature = {'tipo_veh'  : elem['tipo_veh'],
                   'estado' : elem['estado'],
                   'pos' : elem['posicion']
            }
            features.append(feature)
    else: # si es vehiculo
        for elem in data:
            feature = {'vehiculo_id'  : elem['vehiculo_id'],
                   'pos' : elem['posicion'],
                   'tipo': elem['tipo']    
            }
            features.append(feature)
            
    return json.dumps(features)

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", 
                     str(self.path), str(self.headers))
        self._set_response()
        model.step()
        data = model.status()
        # obtener los datos del modelo...
        resp = ("{"+"\"admin\":" + features(data["admin"],'admin') + ",\"vehiculos\":" + 
               features(data["vehiculos"],"vehiculos") + 
               ",\"cajones\":"+ features(data['cajones'],"cajones") +"}")
        
        self.wfile.write(resp.encode('utf-8'))

    def do_POST(self):
        pass

def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    public_url = ngrok.connect(port).public_url
    logging.info(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL + C stops the server
        pass

    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    # server
    run(HTTPServer, Server)
