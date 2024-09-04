import argparse
from caching_proxy import start_server, clear_cache

def main():
    parser = argparse.ArgumentParser(description="Start a caching proxy server.")
    parser.add_argument('--port', type=int, help="Port on which the server will run")
    parser.add_argument('--origin', type=str, help="Origin URL to which requests will be forwarded")
    parser.add_argument('--clear-cache', action='store_true', help="Clear the cache")

    args = parser.parse_args()

    if args.clear_cache:
        clear_cache()
    elif args.port and args.origin:
        start_server(args.port, args.origin)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
