import paramiko


class SFTP_Connection:
    def __init__(self, hostname=None, port=22, username=None, key_path=None, base_dir="./"):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.base_dir = base_dir
        self.key = paramiko.Ed25519Key.from_private_key_file(key_path)

        self.connect()

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.ssh_client.connect(self.hostname, self.port, self.username, pkey=self.key)
        self.ssh_client.get_transport().set_keepalive(90) #seconds

        self.sftp = self.ssh_client.open_sftp()

    def list_files(self, path="."):
        return self.sftp.listdir(path)

    def put(self, filelike, filename, remotedir=None):
        if remotedir is None:
            remotedir = self.base_dir
        remotepath = f"{remotedir}/{filename}"
        return self.sftp.putfo(filelike, remotepath)

    def close(self):
        self.sftp.close()
        self.ssh_client.close()
