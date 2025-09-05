import os, time, datetime

IN_FILE  = os.getenv("IN_FILE", "/shared/requests.log")
OUT_FILE = os.getenv("OUT_FILE", "/shared/aggregated.log")

os.makedirs("/shared", exist_ok=True)
open(IN_FILE, "a").close()
open(OUT_FILE, "a").close()

def tail(fname):
    with open(fname, "r", encoding="utf-8") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line

if __name__ == "__main__":
    for line in tail(IN_FILE):
        stamp = datetime.datetime.utcnow().isoformat() + "Z"
        with open(OUT_FILE, "a", encoding="utf-8") as out:
            out.write(f"[{stamp}] {line}")
        print(f"logged: {line.strip()}")
