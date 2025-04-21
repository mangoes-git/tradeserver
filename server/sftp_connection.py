import paramiko


class SFTP_Connection:
    def __init__(self, hostname=None, port=22, username=None, key_path=None):
        my_key = paramiko.Ed25519Key.from_private_key_file(key_path)

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname, port, username, pkey=my_key)

        self.sftp = self.ssh_client.open_sftp()

    def list_files(self, path="."):
        return self.sftp.listdir(path)

    def put(self, filelike, filename, remotedir="/."):
        remotepath = f"{remotedir}/{filename}"
        return self.sftp.putfo(filelike, remotepath)

    def close(self):
        self.sftp.close()
        self.ssh_client.close()
