import subprocess


def run_command_in_directory(command, directory=None):
    full_command = f"source $HOME/.cargo/env && {command}"

    process = subprocess.Popen(
        full_command,
        shell=True,
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(stderr.decode('utf-8'))
    else:
        return stdout.decode('utf-8')
