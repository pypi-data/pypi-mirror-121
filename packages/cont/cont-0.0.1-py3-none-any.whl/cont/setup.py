import os
import shutil
from pathlib import Path
import urllib.request
from tempfile import mkstemp

CRUN_URL = "https://github.com/containers/crun/releases/download/1.1/crun-1.1-linux-amd64-disable-systemd"

CONFIG_DIRS = {"bin": Path("~", ".cont", "bin").expanduser()}

CRUN_PATH = Path(CONFIG_DIRS["bin"], "crun")


class Setup:
    def download_crun(self):
        fd, tempfilename = mkstemp()
        urllib.request.urlretrieve(CRUN_URL, tempfilename)
        mode = "755"
        os.chmod(tempfilename, int(mode, base=8))
        shutil.move(tempfilename, CRUN_PATH)
        os.close(fd)

    def setup(self):
        print("Setting up")
        for conf_dir in CONFIG_DIRS.values():
            os.makedirs(conf_dir, exist_ok=True)
        if not CRUN_PATH.exists():
            print("CRUN is missing")
            self.download_crun()
