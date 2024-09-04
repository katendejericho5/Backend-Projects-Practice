import os
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Global variable to hold the cache directory
CACHE_DIR = "cache"

def clear_cache():
    """Clear the cache by deleting the cache directory."""
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        print("Cache cleared.")
    else:
        print("Cache is already empty.")

class CachingProxyHandler(BaseHTTPRequestHandler):
    """Handler for the caching proxy server."""
    
    def __init__(self, *args, origin=None, **kwargs):
        self.origin = origin
        super().__init__(*args, **kwargs)

    def do_GET(self):
        cache_file_path = os.path.join(CACHE_DIR, self.path.strip("/"))
        if os.path.exists(cache_file_path):
            self._serve_from_cache(cache_file_path)
        else:
            self._forward_request_to_origin()

    def _serve_from_cache(self, cache_file_path):
        """Serve the response from the cache."""
        with open(cache_file_path, 'rb') as cached_file:
            cached_content = cached_file.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('X-Cache', 'HIT')
            self.end_headers()
            self.wfile.write(cached_content)

    def _forward_request_to_origin(self):
        """Forward the request to the origin server and cache the response."""
        try:
            origin_url = self.origin + self.path
            req = Request(origin_url)
            response = urlopen(req)
            content = response.read()

            # Cache the response
            cache_file_path = os.path.join(CACHE_DIR, self.path.strip("/"))
            os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
            with open(cache_file_path, 'wb') as cache_file:
                cache_file.write(content)

            # Respond with the content
            self.send_response(response.status)
            for key, value in response.getheaders():
                self.send_header(key, value)
            self.send_header('X-Cache', 'MISS')
            self.end_headers()
            self.wfile.write(content)

        except (HTTPError, URLError) as e:
            self.send_error(500, str(e))

def start_server(port, origin):
    """Start the caching proxy server."""
    def handler(*args, **kwargs):
        CachingProxyHandler(*args, origin=origin, **kwargs)
    
    with HTTPServer(('', port), handler) as server:
        print(f"Starting server on port {port} with origin {origin}")
        server.serve_forever()
