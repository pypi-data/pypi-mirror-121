import paramiko

from src.eztransfer.base import BaseHandle
from src.eztransfer.util import typename, insert_logger


@insert_logger
class SFTPHandle(BaseHandle):
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh_client = ssh_client

        self._sftp_client = None

    @property
    def client(self):
        return self._sftp_client

    def connect(self):
        self._open_ssh()
        self._open_sftp()
        self.logger.info(f"Connected")

    def disconnect(self):
        self.client.close()
        self._ssh_client.close()
        self.logger.info(f"Disconnected")

    def download(self, remote_path: str, local_path: str):
        self.client.get(remote_path, local_path)
        self.logger.info(f"File {remote_path!r} downloaded")
        return local_path

    def upload(self, local_path: str, remote_path: str):
        self.client.put(local_path, remote_path)
        self.logger.info(f"File {local_path!r} uploaded to {remote_path!r}")

    def _open_ssh(self):
        self._ssh_client.connect(self._host, self._port, self._username, self._password)

    def _open_sftp(self):
        self._sftp_client = self._ssh_client.open_sftp()

    def __repr__(self):
        return (f"{typename(self)}(host={self._host!r}, username={self._username!r}, "
                f"password={self._password!r}, port={self._port!r})")
