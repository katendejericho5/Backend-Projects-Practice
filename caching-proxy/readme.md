# Caching Proxy Server with Flask

## Introduction

This project is a **caching proxy server** built using Python and Flask. The server forwards requests from clients (like your web browser) to another server (called the "origin server"). If the same request is made again, it returns the cached (stored) response instead of contacting the origin server again. This helps reduce load on the origin server and speeds up response times.

### Key Concepts

1. **Proxy Server:** A server that acts as an intermediary between a client (you) and another server (origin server).
2. **Caching:** Storing data temporarily to serve future requests faster.
3. **Flask:** A lightweight web framework in Python for building web servers.
4. **HTTP Methods:** GET, POST, PUT, DELETE - ways to send and receive data between a client and server.

## Requirements

To run this project, you'll need:

- **Python 3.8+** installed on your computer.
- **Flask** web framework. You can install it by running:
  ```
  pip install Flask
  ```
- **Requests** module, which helps send HTTP requests easily. Install it by running:
  ```
  pip install requests
  ```

## How It Works

### Step 1: Start the Server

To start the server, run the following command in your terminal:

```bash
python caching_proxy.py --port <number> --origin <url>
```

- **--port**: The port number where your proxy server will listen (e.g., 3000).
- **--origin**: The URL of the server to which the requests will be forwarded (e.g., `http://dummyjson.com`).

### Example

```bash
python caching_proxy.py --port 3000 --origin http://dummyjson.com
```

This command starts the caching proxy server on port `3000` and forwards requests to `http://dummyjson.com`.

### Step 2: Make a Request

After starting the server, you can make a request to it.

Example:

- Open your web browser and go to `http://localhost:3000/products`.
- The proxy server will forward this request to `http://dummyjson.com/products`.
- The response will be cached, and if you visit `http://localhost:3000/products` again, you'll get the cached response.

### Step 3: Cache Hit or Miss

When a response is served from the cache, the server adds a header:

- **X-Cache: HIT** (if the response is from the cache).
- **X-Cache: MISS** (if the response is from the origin server).

This helps you know where the response came from.

### Step 4: Clearing the Cache

To clear the cache, run the following command:

```bash
python caching_proxy.py --clear-cache
```

This will remove all stored responses, and the next request will fetch fresh data from the origin server.

## Code Explanation

### Imports

```python
from flask import Flask, request, jsonify
import requests
import hashlib
```

- **Flask:** To create a web server.
- **request:** To access details of incoming requests.
- **requests:** To forward requests to the origin server.
- **hashlib:** To generate a unique key for each request for caching purposes.

### Routes

```python
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Code for forwarding the request and caching the response.
```

- **`@app.route('/<path:path>')`:** This captures any URL after the base URL and forwards it to the origin server.
- **Handling Methods (GET, POST, PUT, DELETE):** Depending on the request method, the corresponding request is made to the origin server.

### Caching Mechanism

```python
cache_key = hashlib.md5(url.encode()).hexdigest()
cache[cache_key] = response.json()
```

- **hashlib.md5(url.encode()).hexdigest():** Generates a unique key based on the URL to store the response.
- **cache[cache_key]:** Stores the response in a cache dictionary.

### Error Handling

The code uses a try-except block to handle errors gracefully. If the origin server is down or an error occurs, the server will return an appropriate message.

### Clearing the Cache

```python
@app.cli.command('clear-cache')
def clear_cache():
    global cache
    cache = {}
    print("Cache cleared!")
```

- **`@app.cli.command('clear-cache')`:** This allows you to clear the cache from the command line.

## Testing Your Server

1. Start the server.
2. Open your browser and make a request.
3. Refresh the page to see if the cache is working (the second request should be faster).
4. Clear the cache using the command and test again.
