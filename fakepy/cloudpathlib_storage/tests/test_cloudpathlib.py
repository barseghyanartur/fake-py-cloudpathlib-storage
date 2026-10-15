"""cloudpathlib regression tests."""

from unittest.mock import Mock

import pytest
from cloudpathlib.local import (
    LocalAzureBlobClient,
    LocalGSClient,
    LocalS3Client,
)
from fake import FAKER, FILE_REGISTRY

from ..aws_s3 import AWSS3Storage
from ..azure_cloud_storage import AzureCloudStorage
from ..cloud import (
    CloudpathlibFileSystemStorage,
    CloudStorage,
    LocalFileSystemStorage,
)
from ..google_cloud_storage import GoogleCloudStorage


@pytest.fixture(params=["local", "s3", "gs", "az"])
def storage(request, tmp_path):
    if request.param == "local":
        return LocalFileSystemStorage("bucket", local_storage_dir=tmp_path)
    cls, client_cls = {
        "s3": (AWSS3Storage, LocalS3Client),
        "gs": (GoogleCloudStorage, LocalGSClient),
        "az": (AzureCloudStorage, LocalAzureBlobClient),
    }[request.param]
    options = (
        {"connection_string": "local-test"} if request.param == "az" else {}
    )
    return cls(
        "bucket", client=client_cls(local_storage_dir=tmp_path, **options)
    )


@pytest.mark.parametrize("kind", ["path", "string", "uri", "relative"])
def test_roundtrip(storage, kind):
    path = storage.generate_filename("txt", basename="hello world")
    name = {
        "path": path,
        "string": str(path),
        "uri": storage.abspath(path),
        "relative": storage.relpath(path),
    }[kind]
    assert storage.write_text(name, "hél lo", encoding="utf-8") == 6
    assert path.read_text(encoding="utf-8") == "hél lo"
    assert storage.write_bytes(name, b"binary") == 6
    assert path.read_bytes() == b"binary"
    assert storage.exists(name)
    storage.unlink(name)
    assert not storage.exists(name)


@pytest.mark.parametrize(
    "method", ["pdf_file", "docx_file", "png_file", "txt_file"]
)
def test_fake_file_registry(storage, method):
    filename = getattr(FAKER, method)(storage=storage)
    assert storage.exists(filename)
    FILE_REGISTRY.clean_up()
    assert not storage.exists(filename)


def test_empty_paths_and_prefix(storage):
    storage.root_path = ""
    storage.rel_path = ""
    filename = storage.generate_filename("txt", prefix="hello_")
    assert filename.name.startswith("hello_")
    assert storage.relpath(filename) == filename.name
    assert filename.parent == storage.bucket


def test_missing_unlink(storage):
    with pytest.raises(FileNotFoundError):
        storage.unlink(storage.generate_filename("txt"))


def test_alias():
    assert CloudpathlibFileSystemStorage is LocalFileSystemStorage


def test_validation():
    with pytest.raises(ValueError):
        CloudStorage("bucket")
    with pytest.raises(ValueError):
        LocalFileSystemStorage("")
    with pytest.raises(ValueError):
        AWSS3Storage("bucket", client=Mock(), credentials={"key_id": "key"})
    with pytest.raises(ValueError):
        LocalFileSystemStorage("bucket").exists("file://remote/path")


@pytest.mark.parametrize(
    "module,name,cls,credentials,expected",
    [
        (
            "aws_s3",
            "S3Client",
            AWSS3Storage,
            {"key_id": "id", "key_secret": "secret"},
            {"aws_access_key_id": "id", "aws_secret_access_key": "secret"},
        ),
        (
            "google_cloud_storage",
            "GSClient",
            GoogleCloudStorage,
            {"json_file_path": "service.json"},
            {"application_credentials": "service.json"},
        ),
        (
            "azure_cloud_storage",
            "AzureBlobClient",
            AzureCloudStorage,
            {"connection_string": "connection"},
            {"connection_string": "connection"},
        ),
    ],
)
def test_credentials_translation(
    monkeypatch, module, name, cls, credentials, expected
):
    import importlib

    target = importlib.import_module("fakepy.cloudpathlib_storage." + module)
    factory = Mock()
    monkeypatch.setattr(target, name, factory)
    storage = cls("bucket", credentials=credentials)
    factory.assert_called_once_with(**expected)
    factory.return_value.CloudPath.assert_called_with(
        f"{storage.schema}://bucket"
    )
    storage.authenticate(**credentials)
    assert factory.call_count == 2


def test_client_options(monkeypatch):
    from .. import aws_s3

    factory = Mock()
    monkeypatch.setattr(aws_s3, "S3Client", factory)
    AWSS3Storage(
        "bucket", client_kwargs={"endpoint_url": "http://localhost:9000"}
    )
    factory.assert_called_once_with(endpoint_url="http://localhost:9000")


def test_instance_client_isolation(tmp_path):
    first = AWSS3Storage(
        "bucket", client=LocalS3Client(local_storage_dir=tmp_path / "a")
    )
    second = AWSS3Storage(
        "bucket", client=LocalS3Client(local_storage_dir=tmp_path / "b")
    )
    path = first.generate_filename("txt", basename="same")
    first.write_text(path, "one")
    assert not second.exists(second.generate_filename("txt", basename="same"))
