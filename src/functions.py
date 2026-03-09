import json
import pathlib
import subprocess
import shlex
import shutil
import sys
import tempfile

DLP_DIR = pathlib.Path("src") / "yt-dlp"

def getConfig():
    with open("config.json", "r") as x:
        return json.loads(x.read())

def getRuntime():
    config = getConfig()
    runtime = config.get("js-runtime")
    path = config.get("js-runtime-path")
    if runtime not in ["deno", "quickjs", "node"]:
        return False
    if path:
        p = pathlib.Path(path)
        if p.exists():
            return f"{runtime}:{p}"
    if shutil.which(runtime):
        return runtime

    return False

def download(commandline : str, url : str):
    print(url)
    with tempfile.TemporaryDirectory() as cache:
        downloadF = getConfig()["downloadFolder"]
        subprocess.run([
            sys.executable,
            DLP_DIR,
            *shlex.split(commandline),
            "-o",
            f"{downloadF}/%(title)s.%(ext)s",
            url
        ])


def ytsearch(query: str, limit: int):
    content = {
        "title": [],
        "url": []
    }
    results = subprocess.run(
        [sys.executable,
        DLP_DIR,
        "--print",
        "%(title)s::SPLITTHHISS::%(webpage_url)s",
        "--skip-download",
        "--flat-playlist",
        "--js-runtime",
        getRuntime(),
        f"ytsearch{limit}:{query}"],
        capture_output=True,
        text=True
    ).stdout.strip().splitlines()

    for line in results:
        if "::SPLITTHHISS::" in line:
            title, url = line.split("::SPLITTHHISS::", 1)
            content["title"].append(title.strip())
            content["url"].append(url.strip())
    return content