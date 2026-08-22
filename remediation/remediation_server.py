#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080
LOG = "/var/log/sre-remediation.log"


class RemediationHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/remediate":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
        except Exception:
            self.send_response(400)
            self.end_headers()
            return

        alerts = payload.get("alerts", [])

        for alert in alerts:
            alertname = alert.get("labels", {}).get("alertname")

            if alertname == "NodeExporterDown":
                with open(LOG, "a") as f:
                    f.write(
                        f"{datetime.now()} - "
                        f"Received NodeExporterDown alert. "
                        f"Starting remediation.\n"
                    )

                subprocess.run(
                    ["/usr/local/bin/remediate_node_exporter.sh"],
                    check=False
                )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Remediation processed\n")

    def log_message(self, format, *args):
        return


server = HTTPServer((HOST, PORT), RemediationHandler)

print(f"Remediation server listening on {HOST}:{PORT}")

server.serve_forever()
