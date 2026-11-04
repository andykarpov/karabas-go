#!/usr/bin/env python3
# Copies the .kg of each core repo listed in cores.json into cores/ when it differs, one git
# commit per core: "<Core name> build <build>: <subject of the core commit> (<repo>@<sha>)".
# Only a file that is a valid kgo2 core (karabas-go-tools docs/kgo2.md) with the id of the one in
# cores/ is taken. The core repos are public: no token is needed to read them (GITHUB_TOKEN, when
# set, only raises the API rate limit).
#
# Usage: python3 .github/scripts/sync_cores.py [--only <file.kg>] [--dry-run]
# Run from the root of the repo. Commits, does not push.

import argparse
import json
import os
import struct
import subprocess
import sys
import urllib.request

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "karabas-go-sync-cores"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith(API):
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else json.loads(data)


# the id, name and build of a kgo2 file (its CORE section, the strings of any board), or None
def kg2_info(data):
    if len(data) < 32 or data[:4] != b"kgo2":
        return None
    _, version, _, hsize, count, esize, mask = struct.unpack_from("<4sBBHHHH", data, 0)
    if hsize < 32 or esize < 16 or count == 0 or hsize + count * esize > len(data) or not mask:
        return None
    strings = core = None
    for i in range(count):
        t, _, ofs, ln = struct.unpack_from("<HHII", data, hsize + i * esize)
        if ofs + ln > len(data):
            return None
        if t == 1 and strings is None:
            strings = data[ofs:ofs + ln]
        elif t == 2 and core is None:
            core = data[ofs:ofs + ln]
    if strings is None or core is None or len(core) < 16:
        return None

    def s(ref):
        end = strings.find(b"\0", ref)
        return strings[ref:end].decode("utf-8", "replace") if 0 <= ref < len(strings) and end >= 0 else ""

    _, i, n, b = struct.unpack_from("<HHHH", core, 0)
    return {"id": s(i), "name": s(n), "build": s(b), "boards": mask}


def git(*args):
    return subprocess.run(["git"] + list(args), check=True, capture_output=True, text=True).stdout


def main():
    parser = argparse.ArgumentParser(description="copy the .kg of the core repos into cores/")
    parser.add_argument("--only", help="one file of cores.json")
    parser.add_argument("--dry-run", action="store_true", help="report, change nothing")
    args = parser.parse_args()

    cores = json.load(open("cores.json"))["cores"]
    if args.only:
        cores = [c for c in cores if c["file"] == args.only]
        if not cores:
            sys.exit("%s is not in cores.json" % args.only)
    changed, errors = 0, 0
    for c in cores:
        where = "%s@%s:%s" % (c["repo"], c["branch"], c["path"])
        try:
            data = get("%s/%s/%s/%s" % (RAW, c["repo"], c["branch"], c["path"]), binary=True)
        except Exception as e:
            print("%s: %s: cannot download (%s)" % (c["file"], where, e))
            errors += 1
            continue
        dst = os.path.join("cores", c["file"])
        old = open(dst, "rb").read() if os.path.isfile(dst) else None
        if old == data:
            print("%s: up to date" % c["file"])
            continue
        info = kg2_info(data)
        if info is None:
            print("%s: %s is not a valid kgo2 core file, skipped" % (c["file"], where))
            errors += 1
            continue
        old_info = kg2_info(old) if old else None
        if old_info and old_info["id"] != info["id"]:
            print("%s: the core id changed (%s -> %s), skipped" % (c["file"], old_info["id"], info["id"]))
            errors += 1
            continue
        commits = get("%s/repos/%s/commits?sha=%s&path=%s&per_page=1" % (API, c["repo"], c["branch"], c["path"]))
        sha = commits[0]["sha"][:7] if commits else "?"
        subject = commits[0]["commit"]["message"].splitlines()[0] if commits else ""
        if subject.startswith("Merge pull request") and commits:
            body = [l for l in commits[0]["commit"]["message"].splitlines()[1:] if l.strip()]
            subject = body[0] if body else subject
        msg = "%s build %s: %s (%s@%s)" % (info["name"] or info["id"], info["build"], subject, c["repo"].split("/")[-1], sha)
        print("%s: %s -> %s" % (c["file"], old_info["build"] if old_info else "new", info["build"]))
        if args.dry_run:
            continue
        with open(dst, "wb") as f:
            f.write(data)
        git("add", dst)
        git("commit", "-q", "-m", msg)
        changed += 1
    print("%d core(s) updated, %d problem(s)" % (changed, errors))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
