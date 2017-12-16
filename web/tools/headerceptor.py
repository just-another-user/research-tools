# -*- coding: utf-8 -*-
"""
Headerceptor - Headers interceptor
Catch and display all http requests' headers.

Based on https://gist.github.com/phrawzty/62540f146ee5e74ea1ab

TODO:
    - Add https support
"""
# SOURCE = https://gist.github.com/phrawzty/62540f146ee5e74ea1ab
import logging
import argparse
import http.server
import socketserver

__author__ = "just-another-user"
__version__ = "1.0"
__last_updated__ = "16/12/2017"

HOST = "127.0.0.1"
PORT = 8000


# noinspection PyPep8Naming
class Handler(http.server.SimpleHTTPRequestHandler):

    def do_HEAD(self):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
        logging.info(self.headers)

    do_GET = do_OPTIONS = do_PUT = do_DELETE = do_POST = do_PATCH = do_HEAD


def get_args():
    parser = argparse.ArgumentParser(prog='headerceptor.py',
                                     description='Listen on a local port and print the incoming request headers')
    parser.add_argument('-o', '--output', action='store', metavar='OUTPUT_FILE', dest='out_file',
                        help="Save output to OUTPUT_FILE. "
                             "Log will still show on screen unless used with the -q flag")
    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                        help="Do not print output to the screen. "
                             "Should be used together with -o, otherwise what's the point?")
    parser.add_argument('-p', '--port', action='store', dest='port', default=PORT,
                        help="Port for localhost to listen on. Defaults to {}".format(PORT))
    return parser.parse_args()


def main():
    args = get_args()

    if 'output' in args:    # Setup the optional output file
        logging.basicConfig(format="%(message)s".format(), level=logging.INFO, filename=args.output)

        if not args.quiet:  # Output to screen unless the -q flag is selected
            stdout_hndlr = logging.StreamHandler()
            stdout_hndlr.setLevel(logging.INFO)
            stdout_hndlr.setFormatter(logging.Formatter(fmt="%(message)s"))
            logging.getLogger().addHandler(stdout_hndlr)
    else:
        logging.basicConfig(format="%(message)s".format(), level=logging.INFO)

    logging.info("Headerceptor v{} ({})".format(__version__, __last_updated__))

    httpd = socketserver.TCPServer((HOST, args.port), Handler)
    logging.info("[+] Listening on {}:{}... Use ctrl+c to exit".format(HOST, args.port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("[-] Shutting down...")


if __name__ == "__main__":
    main()
