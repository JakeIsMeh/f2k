import PyInstaller.__main__
import subprocess
import time
import sys

def gitHash() -> str:
    return subprocess.check_output(["git", "describe", "--always"]).decode("ascii").strip()

with open("src/buildInfo.py", "w") as f:
    f.write("\n".join([
        f"gitHash = \"{gitHash()}\"",
        f"buildDate = \"{time.asctime(time.gmtime(time.time()))} +00:00\""
    ]))

buildOpts = [
    "src/main.py",
    "--onefile",
    "--name=f2k.exe",
    "--windowed"
]

if "clean" in sys.argv:
    buildOpts += ["--clean"]

PyInstaller.__main__.run(buildOpts)