import subprocess

from clio.shell import Shell


class Minerva:
    @staticmethod
    def are_prerequisites_installed() -> bool:
        check_existence_in_minerva_command = "sudo kubectl exec -it deployment/minerva -c minerva -- /bin/sh -c "
        rsync_process = Shell.run(check_existence_in_minerva_command + ' "rsync"')
        openssh_process = Shell.run(check_existence_in_minerva_command + '"openssh"')
        if rsync_process.returncode != 0:
            return False
        if openssh_process.returncode != 0:
            return False
        return True

    @staticmethod
    def install_prerequisites():
        command = 'sudo kubectl exec -it deployment/minerva -c minerva -- /bin/sh -c "apk add rsync openssh"'
        subprocess.run([command], shell=True)
