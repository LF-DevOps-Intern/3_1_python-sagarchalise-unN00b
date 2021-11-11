#!/bin/bash

show_help(){
    echo -ne "usage: $0 url [true|false]\n"
    echo -ne "description:\n"
    echo -ne "\turl \t\tURL to the remote file\n"
    echo -ne "\ttrue|false \tWhether to serve the file after download\n"
}

activate_venv(){
    ENVDIR="$HOME/.venv/pygetremote"

    # Create directory and initialize virtualenv if it doesn't exist
    if [[ ! -d $ENVDIR ]]; then
        mkdir -p $ENVDIR
        virtualenv $ENVDIR -p 3.6
        new=1
    fi

    source $ENVDIR/bin/activate

    if [[ $new ]]; then
        python -m pip install -r requirements.txt
    fi
}

URL=$1
SERVE_FLAG=$2

if [[ $# -eq 0 || "$1" == "-h" ]]; then
    show_help
    exit 0
fi


activate_venv &> /dev/null

if [[ $? -ne 0 ]]; then
    echo "Failed to initialize virtual environment at $ENVDIR"
    exit 1
fi

if [[ "$SERVE_FLAG" == "true" ]]; then
    python3 pgr.py --url=$URL --http_server
else
    python3 pgr.py --url=$URL
fi
