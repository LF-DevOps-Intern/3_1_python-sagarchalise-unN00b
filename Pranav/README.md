### PyGetRemote v0.1b

Simple file downloader and server using Python and Bash.

#### To Install:

*Note: You need to have Python 3 installed on your system.*

1. Clone the repo
2. Run `pgr.sh`

---

The shell script is just a wrapper around the Python script that sets virtual environment, installs required packages, and invokes the program.

### Usage:
 
#### pgr.py

```
usage: pgr.py [-h] [-u URL] [-i] [-P PORT] [-V] [-s] [-p OUT_PATH]
              [-o OUT_FILENAME] [-k]

PyGetRemote 0.1b

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     url to remote file
  -i, --ignore_status   ignore response code
  -P PORT, --port PORT  set server port
  -V, --version         show program version
  -s, --http_server     flag to serve file using HTTP server
  -p OUT_PATH, --path OUT_PATH
                        location to store file locally
  -o OUT_FILENAME, --out OUT_FILENAME
                        override output filename
  -k, --skip_tls        flag to skip SSL/TLS verification (Use at your own
                        risk!)
```

#### pgr.sh
```
usage: ./pgr.sh url [true|false]
description:
	url 		URL to the remote file
	true|false 	Whether to serve the file after download
 ```
