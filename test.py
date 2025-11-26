import subprocess

x = "helloworld"
subprocess.run([f"notify-send {x}"], shell=True)
subprocess.run("echo hello world", shell=True)