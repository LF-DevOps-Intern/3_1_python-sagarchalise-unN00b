#!/usr/bin/env python3

import sys
import requests
import argparse
import os
import uuid
import socketserver
import http.server
from requests.exceptions import HTTPError, ConnectionError, TooManyRedirects, Timeout

parser = argparse.ArgumentParser(description='PyGetRemote 0.1b')

parser.version = 'PyGetRemote 0.1b'
parser.add_argument('-u', '--url', help='url to remote file', type=str)
parser.add_argument('-i', '--ignore_status', help='ignore response code', action='store_true')
parser.add_argument('-P', '--port', help='set server port', type=int)
parser.add_argument('-V', '--version', help='show program version', action='version')
parser.add_argument('-s', '--http_server', help='flag to serve file using HTTP server', action='store_true')
parser.add_argument('-p', '--path', help='location to store file locally', type=str, metavar='OUT_PATH')
parser.add_argument('-o', '--out', help='override output filename', type=str, metavar='OUT_FILENAME')
parser.add_argument('-k', '--skip_tls', help='flag to skip SSL/TLS verification (Use at your own risk!)', action='store_true')

args = parser.parse_args()

out_path = args.path or '.'
url = args.url
http_server_flag = args.http_server
skip_tls_flag = not args.skip_tls
out_file = args.out
serve_port = args.port
ignore_status_code = args.ignore_status

if serve_port and not http_server_flag:
    print('Automatically launching server!')

# Download file
def download_remote(url):
    downloaded_content = None
    filename = None

    # Get filename by parsing url
    filename = url.split('/')[-1] or 'index.html'

    # Send request to server
    try:
        response = requests.get(url, verify=(skip_tls_flag), timeout=5)
        response_status = str(response.status_code)[0]

        # Check status code
        if not ignore_status_code:
            if response_status == '4':
                print('Remote file not found!')
                exit(0)

            elif response_status == '5':
                print('Server error, got 5xx response!')
                exit(0)

        # If redirected, then take the latest redirected URL 
        # and parse new file name
        redirected = len(response.history)
        if redirected:
            print(f'Redirected to {response.history[-1].url}')
            filename = response.history[-1].url.split('/')[-1] or filename

        downloaded_content = response.content

    except ConnectionError:
        print(f'Could not open {URL}')

    except TooManyRedirects:
        print('Received too many redirects!')

    except Timeout:
        print('Connection timed out!')

    except HTTPError as http_error:
        print(f'Unhandled HTTP Error: {http_error}')

    except Exception as e:
        print(e)
        print('Unhandled exception occured while fetching the remote content!')

    if not downloaded_content:
        print('File not downloaded!')

    return (downloaded_content, filename)


# Save to file
def save_file(downloaded_content, filename):
    # Override out_file
    if out_file:
        filename = out_file

    final_path = os.path.join(out_path, filename)

    # Try to create directory if its not present
    if not os.path.exists(out_path):
        try:
            os.makedirs(os.path.join(os.curdir, out_path))
        except Exception as e:
            print(e)
            print(f'Could not create output directory {out_path}')
            print('Saving file to /tmp instead')
            final_path = os.path.join('/tmp', filename)

    try:
        with open(final_path, 'wb') as f:
            f.write(downloaded_content)
        print(f'Saved as {final_path}')
    except Exception as e:
        print(e)
        print('Could not save file!')

    # return out_path
    return final_path


def serve_file(file_path, port):

    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.path = file_path
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    Handler = MyHttpRequestHandler

    try:
        with socketserver.TCPServer(("", port or 8080), Handler) as s:
            print("Serving files")
            s.serve_forever()
    except Exception as e:
        print(e)


def main():
    try:
        serve_directory = save_file(*download_remote(url))
        if http_server_flag:
            serve_file(serve_directory, serve_port)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
