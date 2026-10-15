from typing import Optional

from cloudpathlib import AzureBlobClient

from .cloud import CloudStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("AzureCloudStorage",)


class AzureCloudStorage(CloudStorage):
    """Azure Cloud Storage.

    Usage example:

    .. code-block:: python

        from fakepy.cloudpathlib_storage.azure_cloud_storage import (
            AzureCloudStorage,
        )

        azure_storage = AzureCloudStorage(
            bucket_name="artur-testing-1",
            rel_path="tmp",
        )
        file = azure_storage.generate_filename(prefix="zzz_", extension="txt")
        azure_storage.write_text(file, "Lorem ipsum")
        azure_storage.write_bytes(file, b"Lorem ipsum")
    """

    schema: str = "az"

    def authenticate(
        self: "AzureCloudStorage",
        connection_string: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Authenticate to Azure Cloud Storage.

        Any additional keyword arguments (and `client_kwargs`) are passed
        to `cloudpathlib.AzureBlobClient`.

        :param connection_string: Azure connection string.
        :param \\*\\*kwargs:
        """
        options = dict(self.client_kwargs)
        options.update(kwargs)
        if connection_string is not None:
            options["connection_string"] = connection_string
        self.client = AzureBlobClient(**options)
        if hasattr(self, "bucket"):
            self.bucket = self._make_bucket()
