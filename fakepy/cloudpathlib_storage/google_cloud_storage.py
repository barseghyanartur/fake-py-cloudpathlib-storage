from typing import Optional

from cloudpathlib import GSClient

from .cloud import CloudStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("GoogleCloudStorage",)


class GoogleCloudStorage(CloudStorage):
    """Google Cloud Storage.

    Usage example:

    .. code-block:: python

        from fakepy.cloudpathlib_storage.google_cloud_storage import (
            GoogleCloudStorage,
        )

        gs_storage = GoogleCloudStorage(
            bucket_name="artur-testing-1",
            rel_path="tmp",
        )
        file = gs_storage.generate_filename(prefix="zzz_", extension="txt")
        gs_storage.write_text(file, "Lorem ipsum")
        gs_storage.write_bytes(file, b"Lorem ipsum")
    """

    schema: str = "gs"

    def authenticate(
        self: "GoogleCloudStorage",
        json_file_path: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Authenticate to Google Cloud Storage.

        Any additional keyword arguments (and `client_kwargs`) are passed
        to `cloudpathlib.GSClient`.

        :param json_file_path: Path to the service account JSON file.
        :param \\*\\*kwargs:
        """
        options = dict(self.client_kwargs)
        options.update(kwargs)
        if json_file_path is not None:
            options["application_credentials"] = json_file_path
        self.client = GSClient(**options)
        if hasattr(self, "bucket"):
            self.bucket = self._make_bucket()
