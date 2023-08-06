import atexit
import os
import tempfile
from dataclasses import dataclass

from .base import BaseHandle
from .util import remove_dir, auto_repr, get_logger

logger = get_logger(__name__)


@dataclass(eq=True, frozen=True)
class LocalFile:
    path: str
    filename: str
    size: int

    @classmethod
    def from_path(cls, path: str):
        try:
            return cls(path, os.path.basename(path), os.path.getsize(path))
        except OSError:
            logger.error(f"File {path} does not exist or is inaccessible.")
            raise


@auto_repr
class Transfer:
    def __init__(self, source: BaseHandle, destination: BaseHandle):
        self._source = source
        self._destination = destination
        self._temp_dir = self._create_temp_dir()
        self._source_files = set()
        self._destination_path = None
        self._single_file = False

        self._downloaded_files = set()

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    @property
    def source_files(self):
        return self._source_files

    @property
    def destination_path(self):
        return self._destination_path

    def file(self, path: str):
        self._single_file = True
        return self.files([path])

    def files(self, paths: [str]):
        self._source_files.update(paths)
        return self

    def files_from_directory(self, path: str):
        raise NotImplementedError

    def to(self, path: str):
        self._destination_path = path
        return self

    def execute(self):
        if not (self.source_files and self.destination_path):
            raise ValueError("Source files or destination path is not specified.")

        if self._single_file and len(self.source_files) > 1:
            raise ValueError("Method 'file' was used, but source files container contains more than 1 file.")

        with self.source as src, self.destination as dst:
            for file in self.source_files:
                localpath = os.path.join(self._temp_dir, os.path.basename(file))
                src.download(file, localpath)
                self._add_downloaded_file(localpath)

            if len(os.listdir(self._temp_dir)) != len(self.source_files):
                raise FileNotFoundError("Not all source files were downloaded. Aborting.")

            if self._single_file:
                if len(self._downloaded_files) != 1:
                    raise ValueError("Method 'file' was used, but found more than 1 downloaded file.")

                local_file = next(iter(self._downloaded_files)).path
                dst.upload(local_file, self.destination_path)
            else:
                for file in self._downloaded_files:
                    destination_path = os.path.join(self.destination_path, file.filename)
                    dst.upload(file.path, destination_path)

    def _add_downloaded_file(self, path):
        local_file = LocalFile.from_path(path)
        self._downloaded_files.add(local_file)

    @staticmethod
    def _create_temp_dir():
        temp_dir = tempfile.mkdtemp()
        atexit.register(remove_dir, temp_dir, ignore_errors=True)
        return temp_dir
