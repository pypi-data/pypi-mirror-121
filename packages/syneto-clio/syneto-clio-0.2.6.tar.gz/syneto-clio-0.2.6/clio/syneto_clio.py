import os
import signal
import subprocess
import sys
import threading

import click

from clio.config import Config
from clio.prerequisites.giove import Giove
from clio.prerequisites.minerva import Minerva
from clio.shell import Shell
from clio.kube.container import Container
from clio.path import Path
from clio.sync import Sync, sync_common_options


@click.group()
def cli():
    pass


def keyboardInterruptHandler(signal, frame):
    print("\nKeyboardInterrupt has been caught. Cleaning up...")
    return 0


@cli.command(help="Get the logs of the container")
@click.argument("name")
def logs(name):
    Container.check_existence(name)
    command = f"sudo kubectl logs -f deployment/{name} -c {name}"
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    try:
        return Shell.run(command, without_stdout=True)
    except KeyboardInterrupt:
        click.echo("Exiting logs")
        return 0


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


@cli.group(help="Cleanup commands")
def cleanup():
    pass


@cleanup.command(help="Cleanup unnecessary docker images & containers")
def docker():
    Shell.run_cleanup_command("image")
    Shell.run_cleanup_command("container")


@cli.command(help="Save your SSH credentials for easier use of sync commands")
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
    subprocess.run([f"ssh {name}@{ip}"], shell=True)


@cli.group(help="Synchronize your code")
def sync():
    pass


@sync.command(help="Sync giove code")
@sync_common_options
@click.argument("path")
@click.pass_context
def giove(ctx, path, name=None, password=None, ip=None):
    if not os.path.isfile("./config.txt") or os.path.getsize("./config.txt") == 0:
        if name is None or password is None or ip is None:
            click.echo("Missing config information. Please enter your correct name, password and IP and try again.")
            return
        ctx.invoke(config, name=name, password=password, ip=ip)
    ip, name, password = Config.get_ssh_credentials()
    host = name + "@" + ip
    try:
        Path.exists_remote(host, password, path)
    except Exception as e:
        click.echo(f"While checking the path from the remote host the following error occured: {e}")
        return
    if not Giove.are_prerequisites_installed():
        Giove.install_prerequisites()
    command = Sync.generate_command(username=name, ip=ip, password=password, path=path, service_name="giove")
    return Shell.run(command)


@sync.command(help="Sync minerva code")
@sync_common_options
@click.argument("path")
@click.pass_context
def minerva(ctx, path, name=None, password=None, ip=None):
    if not os.path.isfile("./config.txt") or os.path.getsize("./config.txt") == 0:
        if name is None or password is None or ip is None:
            click.echo("Missing config information. Please enter your correct name, password and IP and try again.")
            return
        ctx.invoke(config, name=name, password=password, ip=ip)
    ip, name, password = Config.get_ssh_credentials()
    host = name + "@" + ip
    try:
        Path.exists_remote(host, password, path)
    except Exception as e:
        click.echo(f"While checking the path from the remote host the following error occured: {e}")
        return
    if not Minerva.are_prerequisites_installed():
        Minerva.install_prerequisites()
    command = Sync.generate_command(username=name, ip=ip, password=password, path=path, service_name="minerva")
    return Shell.run(command)


if __name__ == '__main__':
    cli()
