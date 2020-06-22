import subprocess


def run(cmd):
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()
    except FileNotFoundError:
        raise ValueError("Command '" + cmd[0] + "' not found, is it installed?")

    return o
