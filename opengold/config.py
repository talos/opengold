import uuid
from ConfigParser import SafeConfigParser
import sys

###
#
# CONFIG
#
###
if len(sys.argv) != 2:
    print """
Opengold server must be invoked with a single argument, telling it
which mode from `config.ini` to use:

python opengold/server.py <MODE>

Look at `config.ini` for defined modes. Defaults are `production`,
`staging`, and `test`."""
    exit(1)

MODE = sys.argv[1]
PARSER = SafeConfigParser()

if not len(PARSER.read('config.ini')):
    print "No config.ini file found in this directory.  Writing a config..."

    modes = ['production', 'staging', 'test']
    for i in range(0, len(modes)):
        mode = modes[i]
        PARSER.add_section(mode)
        PARSER.set(mode, 'db', str(i))
        PARSER.set(mode, 'js_path', '/js/build')
        PARSER.set(mode, 'cookie_secret', str(uuid.uuid4()))
        PARSER.set(mode, 'longpoll_timeout', '20')
        PARSER.set(mode, 'recv_spec', 'ipc://opengold:1')
        PARSER.set(mode, 'send_spec', 'ipc://opengold:0')

    try:
        conf = open('config.ini', 'w')
        PARSER.write(conf)
        conf.close()
    except IOError:
        print "Could not write config file to `config.ini`, exiting..."
        exit(1)

DB = int(PARSER.get(MODE, 'db'))
JS_PATH = PARSER.get(MODE, 'js_path')
COOKIE_SECRET = PARSER.get(MODE, 'cookie_secret')
LONGPOLL_TIMEOUT = int(PARSER.get(MODE, 'longpoll_timeout'))
PORT = int(PARSER.get(MODE, 'port'))
