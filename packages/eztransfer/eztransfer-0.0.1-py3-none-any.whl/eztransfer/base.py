from src.eztransfer.util import typename


class BaseHandle:

    @property
    def instance_name(self):
        return typename(self)

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def download(self, remote_path: str, local_path: str):
        raise NotImplementedError()

    def upload(self, local_path: str, remote_path: str):
        raise NotImplementedError()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __repr__(self):
        return self.instance_name
