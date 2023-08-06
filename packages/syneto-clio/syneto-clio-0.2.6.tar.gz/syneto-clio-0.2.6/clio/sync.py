import click


def sync_common_options(func):
    sync_options = [click.option('--name'), click.option('--password'), click.option('--ip')]
    for option in reversed(sync_options):
        func = option(func)
    return func


class Sync:
    @staticmethod
    def generate_command(username, ip, password, path, service_name: str) -> str:
        command = (
            f"sudo kubectl exec deployment/{service_name} --container {service_name} -- "
            f"/bin/sh -c \"sshpass -p '{password}' rsync -avzh -e ssh"
            f' {username}@{ip}:{path} /home/syneto-{service_name}"'
        )
        return command
