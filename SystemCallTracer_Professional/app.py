from flask import Flask, render_template, jsonify
import subprocess
import json
import os

app = Flask(__name__)
LOG_FILE = 'data/syscall_log.json'

def run_strace():
    process = subprocess.Popen(
        ['strace', '-e', 'trace=all', '-f', '-tt', 'ls'],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    _, stderr = process.communicate()

    syscalls = []
    for line in stderr.splitlines():
        try:
            time_str, rest = line.split(" ", 1)
            name = rest.split('(')[0]
            args = rest.split('(', 1)[1].rsplit(')', 1)[0]
            ret = rest.split('=')[-1].strip()
            syscall = {
                "timestamp": time_str.strip(),
                "name": name.strip(),
                "args": args.strip(),
                "return": ret
            }
            syscalls.append(syscall)
        except:
            continue

    os.makedirs("data", exist_ok=True)
    with open(LOG_FILE, "w") as f:
        for syscall in syscalls:
            f.write(json.dumps(syscall) + "\n")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tracer")
def tracer():
    if not os.path.exists(LOG_FILE):
        run_strace()
    logs = []
    with open(LOG_FILE) as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except:
                continue
    return render_template("tracer.html", syscalls=logs[-50:])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
