import subprocess


class Config:
    @staticmethod
    def create_config_file():
        subprocess.run(["sudo touch config.txt"], shell=True)
        subprocess.run(["sudo chmod 777 config.txt"], shell=True)

    @staticmethod
    def get_ssh_credentials():
        config_file = open("config.txt", "r")
        config_file_content = config_file.readlines()
        name = config_file_content[0].replace("\n", "")
        password = config_file_content[1].replace("\n", "")
        ip = config_file_content[2]
        return ip, name, password
