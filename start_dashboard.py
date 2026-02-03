#!/usr/bin/env python3
"""Start local server and open dashboard in browser."""
import webbrowser
import http.server
import socketserver
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8000

print(f"Starting server at http://localhost:{PORT}")
print(f"Opening dashboard...")
print(f"Press Ctrl+C to stop.\n")

webbrowser.open(f"http://localhost:{PORT}/dashboard.html")

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()
