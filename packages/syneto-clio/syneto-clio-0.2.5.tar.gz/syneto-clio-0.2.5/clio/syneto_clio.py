import os
import click

from clio.config import Config
from clio.prerequisites.giove import Giove
from clio.prerequisites.minerva import Minerva
from clio.shell import Shell
from clio.kube.container import Container

from clio.path import Path

@click.group()
def cli():
    pass


@cli.command(help="Get the logs of the container")
@click.argument("name")
def logs(name):
    Container.check_existence(name)
    command = f"sudo kubectl logs -f deployment/{name} -c {name}"
    return Shell.run(command, without_stdout=True)


@cli.command(help="Enter the container")
@click.argument("name")
def enter(name):
    Container.check_existence(name)
    command = f"sudo kubectl exec -it deployment/{name} -c {name} -- /bin/sh"
    return Shell.run(command, without_stdout=True)


@cli.command(help="Restart the container")
@click.argument("name")
def restart(name):
    Container.check_existence(name)
    container_id = Container.get_id(name)
    command = f"docker container restart {container_id}"
    return Shell.run(command, without_stdout=True)


@cli.command(help="Cleanup unnecessary docker images & containers")
def cleanup_docker():
    Shell.run_cleanup_command("image")
    Shell.run_cleanup_command("container")


@cli.command(help="Save your SSH credentials for easier use of sync commands.")
@click.option("--name")
@click.option("--password")
@click.option("--ip")
def config(name, password, ip):
    Config.create_config_file()
    if name is None or password is None or ip is None:
        click.echo("Missing SSH credentials. Please try again.")
        return
    with open("./config.txt", "w") as config_file:
        config_file.write(name + "\n" + password + "\n" + ip)
    config_file.close()


@cli.command(help="Sync giove code")
@click.option("--name")
@click.option("--password")
@click.option("--ip")
@click.argument("path")
@click.pass_context
def sync_giove(ctx, path, name=None, password=None, ip=None):
    if not os.path.isfile("./config.txt") or os.path.getsize("./config.txt") == 0:
        if name is None or password is None or ip is None:
            click.echo("Missing config information. Please enter your correct name, password and IP and try again.")
            return
        ctx.invoke(config, name=name, password=password, ip=ip)
    ip, name, password = Config.get_ssh_credentials()
    host = name + "@" + ip
    if not Path.exists_remote(host, password, path):
        click.echo("Provided path does not exist.")
        return
    if not Giove.are_giove_prerequisites_installed():
        Giove.install_giove_prerequisites()
    command = (
        f"sudo kubectl exec deployment/giove --container giove -- "
        f"/bin/sh -c \"sshpass -p '{password}' rsync -avzh -e ssh"
        f' {name}@{ip}:{path} /home/syneto-giove"'
    )
    return Shell.run(command)


@cli.command(help="Sync minerva code")
@click.option("--name")
@click.option("--password")
@click.option("--ip")
@click.argument("path")
@click.pass_context
def sync_minerva(ctx, path, name=None, password=None, ip=None):
    if not os.path.isfile("./config.txt") or os.path.getsize("./config.txt") == 0:
        if name is None or password is None or ip is None:
            click.echo("Missing config information. Please enter your correct name, password and IP and try again.")
            return
        ctx.invoke(config, name=name, password=password, ip=ip)
    ip, name, password = Config.get_ssh_credentials()
    host = name + "@" + ip
    if not Path.exists_remote(host, password, path):
        click.echo("Provided path does not exist.")
        return
    if not Minerva.are_minerva_prerequisites_installed():
        Minerva.install_minerva_prerequisites()
    command = (
        f"sudo kubectl exec deployment/minerva --container minerva -- "
        f"/bin/sh -c \"sshpass -p '{password}' rsync -avzh -e ssh"
        f' {name}@{ip}:{path} /home/syneto-minerva"'
    )
    return Shell.run(command)


if __name__ == '__main__':
    cli()
