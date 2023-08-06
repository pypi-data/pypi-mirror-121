import subprocess

from kubetwo.exception import ProcessException


class Common:

    @classmethod
    def run_command(cls, command: str, cwd: str, stdout: bool=True):
        stdout = None if stdout else subprocess.DEVNULL
        try:
            process = subprocess.run(
                command, 
                shell=True, 
                stdout=stdout, 
                stderr=subprocess.PIPE,
                cwd=cwd
            )
            process.check_returncode()
        except subprocess.CalledProcessError:
            raise ProcessException(process.stderr.decode("utf8"))
        