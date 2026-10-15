from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse
from urllib.request import url2pathname

from cloudpathlib import CloudPath
from cloudpathlib.client import Client
from fake import BaseStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "CloudStorage",
    "CloudpathlibFileSystemStorage",
    "LocalFileSystemStorage",
)

DEFAULT_ROOT_PATH = "tmp"
DEFAULT_REL_PATH = "tmp"

FileType = Union[CloudPath, Path, str]


class CloudStorage(BaseStorage):
    """File storage class using cloudpathlib for path handling.

    Cloud buckets (containers) must already exist. Relative string filenames
    are resolved against ``bucket/root_path`` (not ``rel_path``). Pass a
    provider ``client`` to isolate credentials or to use cloudpathlib's
    local test clients.

    Usage example:

    .. code-block:: python

        from fake import FAKER
        from fakepy.cloudpathlib_storage import LocalFileSystemStorage

        storage = LocalFileSystemStorage(bucket_name="bucket_name")
        docx_file = FAKER.docx_file(storage=storage)

    Initialization with params:

    .. code-block:: python

        from fake import FAKER
        from fakepy.cloudpathlib_storage import LocalFileSystemStorage

        storage = LocalFileSystemStorage(bucket_name="bucket_name")
        docx_file = storage.generate_filename(prefix="zzz_", extension="docx")
        storage.write_bytes(docx_file, FAKER.docx())
    """

    bucket_name: str
    bucket: Union[CloudPath, Path]
    credentials: Dict[str, Any]
    client_kwargs: Dict[str, Any]
    client: Optional[Client]
    schema: Optional[str] = None

    def __init__(
        self: "CloudStorage",
        bucket_name: str,
        root_path: Optional[str] = DEFAULT_ROOT_PATH,
        rel_path: Optional[str] = DEFAULT_REL_PATH,
        credentials: Optional[Dict[str, Any]] = None,
        *args,
        client: Optional[Client] = None,
        client_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        """
        :param bucket_name: Bucket name.
        :param root_path: Path of your files root directory (e.g., Django's
            `settings.MEDIA_ROOT`).
        :param rel_path: Relative path (from root directory).
        :param credentials: Dictionary of credentials.
        :param \\*args:
        :param client: Ready-to-use cloudpathlib client. Mutually exclusive
            with `credentials` and `client_kwargs`.
        :param client_kwargs: Extra keyword arguments for the cloudpathlib
            client.
        :param \\*\\*kwargs:
        :raises ValueError: If `schema` is not set, `bucket_name` is empty,
            or both `client` and `credentials`/`client_kwargs` are given.
        """
        if self.schema is None:
            raise ValueError("The `schema` property should be set!")
        if not bucket_name:
            raise ValueError("bucket_name must not be empty")
        self.bucket_name = bucket_name
        self.root_path = root_path or ""
        self.rel_path = rel_path or ""
        self.cache_dir = None
        self.credentials = dict(credentials or {})
        self.client_kwargs = dict(client_kwargs or {})
        if client is not None and (self.credentials or self.client_kwargs):
            raise ValueError("Pass either client or credentials/client_kwargs")
        self.client = client
        if self.client is None:
            self.authenticate(**self.credentials)
        self.bucket = self._make_bucket()
        super().__init__(*args, **kwargs)

    @abstractmethod
    def authenticate(self, *args, **kwargs):
        raise NotImplementedError("Method authenticate is not implemented!")

    def _make_bucket(self: "CloudStorage") -> Union[CloudPath, Path]:
        """Make bucket path."""
        return self.client.CloudPath(f"{self.schema}://{self.bucket_name}")

    def _get_file(
        self: "CloudStorage",
        filename: FileType,
    ) -> Union[CloudPath, Path]:
        """Get file from path.

        By concept, the path is always relative to the root directory, thus
        `rel_path` + initial filename, when used in string representation.

        :param filename: File name.
        :return: File object.
        :rtype: Union[CloudPath, Path]
        """
        if isinstance(filename, (CloudPath, Path)):
            return filename
        filename = str(filename)
        if filename.startswith(f"{self.schema}://"):
            return self.client.CloudPath(filename)
        return self.bucket / self.root_path / filename

    def generate_filename(
        self: "CloudStorage",
        extension: str,
        prefix: Optional[str] = None,
        basename: Optional[str] = None,
    ) -> Union[CloudPath, Path]:
        """Generate filename."""
        if not extension:
            raise ValueError("Extension shall be given!")

        if not basename:
            basename = self.generate_basename(prefix)

        return (
            self.bucket
            / self.root_path
            / self.rel_path
            / f"{basename}.{extension}"
        )

    def write_text(
        self: "CloudStorage",
        filename: FileType,
        data: str,
        encoding: Optional[str] = None,
    ) -> int:
        """Write text."""
        file = self._get_file(filename)
        if isinstance(file, Path):
            file.parent.mkdir(parents=True, exist_ok=True)
        return file.write_text(data, encoding=encoding)

    def write_bytes(
        self: "CloudStorage",
        filename: FileType,
        data: bytes,
    ) -> int:
        """Write bytes."""
        file = self._get_file(filename)
        if isinstance(file, Path):
            file.parent.mkdir(parents=True, exist_ok=True)
        return file.write_bytes(data)

    def exists(self: "CloudStorage", filename: FileType) -> bool:
        """Check if file exists."""
        return self._get_file(filename).exists()

    def relpath(self: "CloudStorage", filename: FileType) -> str:
        """Return relative path."""
        file = self._get_file(filename)
        return str(file.relative_to(self.bucket / self.root_path))

    def abspath(self: "CloudStorage", filename: FileType) -> str:
        """Return absolute path (URI)."""
        return self._get_file(filename).as_uri()

    def unlink(self: "CloudStorage", filename: FileType) -> None:
        """Delete the file.

        :param filename: File name.
        :raises FileNotFoundError: If the file does not exist.
        """
        file = self._get_file(filename)
        if not file.exists():
            raise FileNotFoundError(str(file))
        file.unlink()


class LocalFileSystemStorage(CloudStorage):
    """Local FileSystem Storage.

    Uses `pathlib.Path`, since cloudpathlib has no `file://` backend.
    Files live under `local_storage_dir/bucket_name/root_path/rel_path`.
    `local_storage_dir` defaults to the system temporary directory.

    Usage example:

    .. code-block:: python

        from fakepy.cloudpathlib_storage.cloud import LocalFileSystemStorage

        storage = LocalFileSystemStorage(bucket_name="artur-testing-1")
        file = storage.generate_filename(prefix="zzz_", extension="txt")
        storage.write_text(file, "Lorem ipsum")
        storage.write_bytes(file, b"Lorem ipsum")
    """

    schema: str = "file"

    def __init__(
        self: "LocalFileSystemStorage",
        *args,
        local_storage_dir: Optional[Union[str, Path]] = None,
        **kwargs,
    ) -> None:
        """
        :param \\*args:
        :param local_storage_dir: Directory to keep buckets in. Defaults to
            the system temporary directory.
        :param \\*\\*kwargs:
        """
        import tempfile

        self.local_storage_dir = Path(
            local_storage_dir or tempfile.gettempdir()
        ).resolve()
        super().__init__(*args, **kwargs)

    def authenticate(self: "LocalFileSystemStorage", **kwargs) -> None:
        """Authenticate. Does nothing."""

    def _make_bucket(self: "LocalFileSystemStorage") -> Path:
        """Make bucket directory."""
        bucket = (self.local_storage_dir / self.bucket_name).resolve()
        bucket.mkdir(parents=True, exist_ok=True)
        return bucket

    def _get_file(
        self: "LocalFileSystemStorage",
        filename: FileType,
    ) -> Union[CloudPath, Path]:
        """Get file from path.

        :param filename: File name.
        :return: File object.
        :rtype: Union[CloudPath, Path]
        :raises ValueError: If a non-local `file://` URI is given.
        """
        if isinstance(filename, Path):
            return filename
        filename = str(filename)
        if filename.startswith("file://"):
            parsed = urlparse(filename)
            if parsed.netloc not in ("", "localhost"):
                raise ValueError("Only local file URIs are supported")
            return Path(url2pathname(parsed.path))
        return self.bucket / self.root_path / filename


CloudpathlibFileSystemStorage = LocalFileSystemStorage
