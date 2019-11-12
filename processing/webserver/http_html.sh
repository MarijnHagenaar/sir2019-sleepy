#!/usr/bin/env bash
# Make sure the working directory is where the script is
cd "$(dirname "$0")" || exit 1

# If we can't run python, we can't run anything
if ! command -v python &> /dev/null; then
  echo "Python not in path."
  exit 1
fi

# These are all key files. If they're not present, we can't do anything.
if ! [ -d html ] || ! [ -f server.py ] || ! [ -f config.json ]; then
  echo "Required files not found, make sure you're in the right directory."
  exit 1
fi

# This runs before exiting to make sure that the server is stopped and the
#  config is clean.
cleanup() {
  echo -e "\nInterrupt received, stopping..."
  kill "$server_pid"
  rm html/js/config.js
  exit 0
}

# Call the cleanup function when exiting
trap cleanup INT TERM

# Create the HTML config for XHR (html/js/config.js), based on
#  config.json.
python <<EOF
from json import loads
with open('config.json') as f:
  cfg = loads(f.read())
with open('html/js/config.js', 'w') as f:
  f.write('var CONFIG = {\n')
  f.write('"server": "'+cfg['server']+'"\n')
  f.write('}')
EOF

# Start the server and save its PID
python server.py &
server_pid=$!
echo "Server running (pid $server_pid)"
echo "Press Ctrl-C to stop."

# Run until the server stops.
wait
