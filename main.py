import sys

from config import animals_map
from pysyncobj import SyncObj, SyncObjConf

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading

animals_map = {0: "Duck", 1: "Candidate - To be Determined Soon", 2: "Goose"}
node = sys.argv[1]
partner_nodes = sys.argv[2:]


class EmptyStorageNeededForSync(SyncObj):
    def __init__(self, selfAddress, partnerAddrs):
        cfg = SyncObjConf(dynamicMembershipChange=True)
        super(EmptyStorageNeededForSync, self).__init__(selfAddress, partnerAddrs, cfg)


class WebServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"{animal}".encode(encoding="utf_8"))


def run_web_server(host, port):
    webServer = HTTPServer((host, port), WebServer)
    webServer.serve_forever()


def run_web_server_as_separated_thread(node):

    host, port = sys.argv[1].split(":")
    port = int(port) + 1000
    function = threading.Thread(target=run_web_server, args=[host, int(port)])

    function.start()


sync_object = EmptyStorageNeededForSync(node, partner_nodes)

run_web_server_as_separated_thread(node)

while True:
    animal = animals_map[sync_object.getStatus()["state"]]

    print(
        f'uptime: {sync_object.getStatus()["uptime"]} : {sync_object.getStatus()["self"]}: {animals_map[sync_object.getStatus()["state"]]}',
    )
    time.sleep(1)
