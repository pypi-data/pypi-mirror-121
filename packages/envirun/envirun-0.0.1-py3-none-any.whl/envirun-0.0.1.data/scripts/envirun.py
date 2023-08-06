#!python

import sys
import os
import subprocess
from dotenv import load_dotenv

if len(sys.argv) < 3:
    print("Load environment file and run program with that environment")
    print("Usage: {} filename.env /path/to/program".format(sys.argv[0]))
    sys.exit(0)

load_dotenv(dotenv_path=sys.argv[1], override=True)
rc = subprocess.run(sys.argv[2:])
sys.exit(rc.returncode)
