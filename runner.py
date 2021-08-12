import subprocess

def subp(cmd):
    process_output = subprocess.run(cmd, shell = True, capture_output = True, text = True)

    return process_output
