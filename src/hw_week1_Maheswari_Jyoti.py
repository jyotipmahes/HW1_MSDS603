import paramiko
from os.path import expanduser
from user_definition import *


git_repo_name = "HW1_MSDS603"
git_user_id = "jyotipmahes"


# ## Assumption : Anaconda, Git (configured)

def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f "
                         "~/HW1_MSDS603/venv/environment.yml")
    if (b'already exists' in stderr.read()):
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f "
                             "~/HW1_MSDS603/venv/environment.yml")


def git_clone(ssh):
    # ---- HOMEWORK ----- #
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        git_clone_command = "git clone https://github.com/" + \
                            git_user_id + "/" + git_repo_name + ".git"
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)
        if (b'already exists' in stderr.read()):
            path_change = "cd /home/ec2-user/"+git_repo_name+"/"
            git_pull_command = "git pull origin master"
            stdin, stdout, stderr = ssh.exec_command(path_change +
                                                     ";" + git_pull_command)


def main():
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)


if __name__ == '__main__':
    main()
