#!/usr/bin/env python3
"""
Simple HTTP server to serve the Celtic Dreamscape page
"""

import http.server
import socketserver
import os
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for better compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Set the port
    PORT = 8000
    
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    # Create the server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🌌 Celtic Dreamscape Server")
        print(f"=" * 50)
        print(f"🚀 Server running at: http://localhost:{PORT}")
        print(f"📄 Celtic Dreamscape: http://localhost:{PORT}/celtic_dreamscape_display.html")
        print(f"🎨 Glyph Curation App: http://localhost:{PORT}/glyph_curation_app.html")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🛑 Press Ctrl+C to stop the server")
        print(f"=" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main() 