from os import name, system
import http.server
import socketserver
import webbrowser
from random import randint

PORT = randint(4040, 8080)

Handler = http.server.SimpleHTTPRequestHandler


def main():
    with socketserver.TCPServer(('127.0.0.1', PORT), Handler) as run:
        if name == 'posix':
            try:
                if webbrowser.open(f'http://127.0.0.1:{PORT}/index.html') == True:
                    pass
                else:
                    system(
                        f'termux-open-url http://127.0.0.1:{PORT}/index.html')
            except:
                print(
                    f"Gagal membuka alamat http://127.0.0.1:{PORT}/index.html")
        else:
            webbrowser.open(f'http://127.0.0.1:{PORT}/index.html')
        try:
            print('CTRL + C , untuk kaluar!')
            run.serve_forever()
        except:
            print('server tidak aktif!')
            run.server_close()
