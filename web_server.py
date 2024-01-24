from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, response_code, response_body):
        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_body).encode('utf-8'))

    def do_GET(self):
        if self.path == '/board':
            lights = self._generate_lights()
            response_body = {'lights': lights}
            self._send_response(200, response_body)
        else:
            response_body = {'message': 'Not Found'}
            self._send_response(404, response_body)

    def _generate_lights(self):
        lights = {'green': [], 'blue': [], 'red': []}

        # Place 1-2 green lights with max height 6
        green_light_count = random.randint(1, 2)
        for _ in range(green_light_count):
            green_light_height = random.randint(1, 6)
            green_light_position = random.randint(0, 17)
            lights['green'].append((green_light_height, green_light_position))

        # Place blue lights everywhere
        for i in range(11):
            for j in range(18):
                if random.choice([True, False]):
                    lights['blue'].append((i + 1, j))

        # Place two red lights at the top of the board
        lights['red'].append((1, random.randint(0, 17)))
        lights['red'].append((1, random.randint(0, 17)))

        return lights

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
