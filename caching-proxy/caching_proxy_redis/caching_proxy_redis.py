import argparse
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Connect to Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_TIMEOUT = 3600  # Cache timeout in seconds

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

class CachingProxyHandler(BaseHTTPRequestHandler):
    """Handler for the caching proxy server."""

    def __init__(self, *args, origin=None, **kwargs):
        self.origin = origin
        super().__init__(*args, **kwargs)

    def do_GET(self):
        cache_key = self.path
        cached_response = redis_client.get(cache_key)
        if cached_response:
            self._serve_from_cache(cached_response)
        else:
            self._forward_request_to_origin()

    def _serve_from_cache(self, cached_response):
        """Serve the response from the cache."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('X-Cache', 'HIT')
        self.end_headers()
        self.wfile.write(cached_response)

    def _forward_request_to_origin(self):
        """Forward the request to the origin server and cache the response."""
        try:
            origin_url = self.origin + self.path
            req = Request(origin_url)
            response = urlopen(req)
            content = response.read()

            # Cache the response
            redis_client.setex(self.path, CACHE_TIMEOUT, content)

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

def clear_cache():
    """Clear the cache by deleting all keys in Redis."""
    redis_client.flushdb()
    print("Cache cleared.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start a caching proxy server.')
    parser.add_argument('--port', type=int, required=True, help='Port for the caching proxy server.')
    parser.add_argument('--origin', type=str, required=True, help='Origin server URL.')
    parser.add_argument('--clear-cache', action='store_true', help='Clear the cache.')

    args = parser.parse_args()

    if args.clear_cache:
        clear_cache()
    else:
        start_server(args.port, args.origin)
