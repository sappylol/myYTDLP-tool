from concurrent.futures import ThreadPoolExecutor
from functools import partial
from os import name, system
import src.functions as functions

commands = ["download", "search", "add", "clear", "help"]
config = functions.getConfig()
downloadList = []

def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def download(url=None):
    workers = config["paralelDownloads"]
    commandline = config["commandline"]

    if not url is None:
        if "https://" in url:
            functions.download(commandline, url)
        else:
            print("seems that this is not a HTTPS url :d")

    worker = partial(functions.download, commandline)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(worker, downloadList))

def search(query=None):
    if query is None:
        print("bro... search for?? 0_o")
        return

    query = str(query)
    resultLimit = config["resultLimit"]
    results = functions.ytsearch(query, config["searchLimit"])

    if not results:
        print("no results")
        return
    total = len(results["title"])
    pages = (total + resultLimit - 1) // resultLimit
    page = 0

    while True:
        start = page * resultLimit
        end = start + resultLimit

        print(f"\npage {page+1}/{pages}\n")

        for i in range(start, min(end, total)):
            print(f"[{i}] {results["title"][i]}")

        cmd = input("\n>>> ").strip().lower().split(" ")

        if cmd[0] == "next":
            clear()
            if page + 1 < pages:
                page += 1
        elif cmd[0] == "back":
            clear()
            if page > 0:
                page -= 1
        elif cmd[0] == "exit":
            break
        elif cmd[0] == "select":
            for number in cmd[1:]:
                if number.isdigit():
                    downloadList.append(results["url"][int(number)])
                    print(f"{number} has selected")
        else:
            print("commands: next | back | exit | select")


def add(url : str):
    if "https://" in url:
        downloadList.append(url)
    else:
        print("seems that this is not a HTTPS url :d") 


def help():
    print("here we go :D\n\ndownload [url:for single download] - starts download proccess by using download list or single url\nsearch [something] - search something in youtube\nadd [url] - it adds to download list an single url per command\nhelp - it helps... displaying the commands\n\nif you want to configurate, just edit the JSON file: 'config.json' before anything\n\nall credits goes to yt-dlp team: https://github.com/yt-dlp/yt-dlp")