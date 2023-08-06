import pipes
import subprocess


class Path:
    @staticmethod
    def exists_remote(host, password, path):
        status = subprocess.call(["sshpass", "-p", password, "ssh", host, "test -e {}".format(pipes.quote(path))])
        if status == 0:
            return True
        if status == 1:
            return False
        raise Exception("SSH failed")
