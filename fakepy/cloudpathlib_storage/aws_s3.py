from typing import Optional

from cloudpathlib import S3Client

from .cloud import CloudStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024-2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("AWSS3Storage",)


class AWSS3Storage(CloudStorage):
    """AWS S3 Storage.

    Usage example:

    .. code-block:: python

        from fakepy.cloudpathlib_storage.aws_s3 import AWSS3Storage

        s3_storage = AWSS3Storage(
            bucket_name="artur-testing-1",
            rel_path="tmp",
        )
        file = s3_storage.generate_filename(prefix="zzz_", extension="txt")
        s3_storage.write_text(file, "Lorem ipsum")
        s3_storage.write_bytes(file, b"Lorem ipsum")
    """

    schema: str = "s3"

    def authenticate(
        self: "AWSS3Storage",
        key_id: Optional[str] = None,
        key_secret: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Authenticate to AWS S3.

        Any additional keyword arguments (and `client_kwargs`) are passed
        to `cloudpathlib.S3Client`.

        :param key_id: AWS access key ID.
        :param key_secret: AWS secret access key.
        :param \\*\\*kwargs:
        """
        options = dict(self.client_kwargs)
        options.update(kwargs)
        if key_id is not None:
            options["aws_access_key_id"] = key_id
        if key_secret is not None:
            options["aws_secret_access_key"] = key_secret
        self.client = S3Client(**options)
        if hasattr(self, "bucket"):
            self.bucket = self._make_bucket()
