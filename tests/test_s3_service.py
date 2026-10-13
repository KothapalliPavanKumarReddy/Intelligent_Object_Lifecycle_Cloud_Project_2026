"""
tests/test_s3_service.py
========================
Unit tests for web/services/s3_service.py.

All tests use unittest.mock to patch boto3 so that no real AWS calls are
made and no real files are uploaded.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from web.services.s3_service import S3Service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_client_error(code: str, message: str = "Simulated error"):
    """Build a minimal botocore ClientError for testing."""
    from botocore.exceptions import ClientError
    return ClientError(
        error_response={"Error": {"Code": code, "Message": message}},
        operation_name="TestOp",
    )


def _service(bucket="test-bucket", region="ap-south-1", profile="") -> S3Service:
    """Return an S3Service with no real AWS profile."""
    return S3Service(bucket=bucket, region=region, profile=profile)


# ---------------------------------------------------------------------------
# upload_file
# ---------------------------------------------------------------------------

class TestUploadFile:

    def test_success_returns_correct_fields(self, tmp_path):
        """Successful upload must return success=True with bucket and key."""
        svc = _service()
        local = tmp_path / "img.jpg"
        local.write_bytes(b"fake")

        mock_client = MagicMock()
        mock_client.upload_file.return_value = None  # boto3 returns None on success
        svc._client = mock_client

        result = svc.upload_file(local)

        assert result["success"] is True
        assert result["bucket"] == "test-bucket"
        assert result["object_key"] == "satellite-images/img.jpg"
        assert result["region"] == "ap-south-1"
        assert str(local) == result["local_path"]

        mock_client.upload_file.assert_called_once_with(
            Filename=str(local),
            Bucket="test-bucket",
            Key="satellite-images/img.jpg",
        )

    def test_custom_object_key_is_used(self, tmp_path):
        """Caller-supplied object_key overrides the default prefix logic."""
        svc = _service()
        local = tmp_path / "img.jpg"
        local.write_bytes(b"fake")
        svc._client = MagicMock()

        result = svc.upload_file(local, object_key="custom/path/img.jpg")

        assert result["success"] is True
        assert result["object_key"] == "custom/path/img.jpg"

    def test_missing_local_file_returns_failure(self):
        """FileNotFoundError from boto3 must yield success=False with an error message."""
        svc = _service()
        svc._client = MagicMock()
        svc._client.upload_file.side_effect = FileNotFoundError("no such file")

        result = svc.upload_file("/nonexistent/path/img.jpg")

        assert result["success"] is False
        assert "not found" in result["error"].lower()
        # Must NOT expose the word 'credential' or any secret-like value
        assert "credential" not in result.get("error", "").lower()

    def test_aws_client_error_returns_failure(self, tmp_path):
        """ClientError from boto3 must yield success=False with a safe error string."""
        svc = _service()
        local = tmp_path / "img.jpg"
        local.write_bytes(b"fake")
        svc._client = MagicMock()
        svc._client.upload_file.side_effect = _make_client_error(
            "AccessDenied", "Access Denied"
        )

        result = svc.upload_file(local)

        assert result["success"] is False
        assert "AccessDenied" in result["error"] or "Access Denied" in result["error"]
        assert "credential" not in result["error"].lower()

    def test_no_credentials_in_error_message(self, tmp_path):
        """Error messages must never contain AWS secret key patterns."""
        svc = _service()
        local = tmp_path / "img.jpg"
        local.write_bytes(b"fake")
        svc._client = MagicMock()
        svc._client.upload_file.side_effect = _make_client_error(
            "InvalidAccessKeyId", "The AWS Access Key Id you provided does not exist"
        )

        result = svc.upload_file(local)

        # Error message is surfaced but must not contain raw secret values
        assert result["success"] is False
        for forbidden in ("AKIA", "secret", "password", "token"):
            assert forbidden.lower() not in result["error"].lower()


# ---------------------------------------------------------------------------
# list_objects
# ---------------------------------------------------------------------------

class TestListObjects:

    def _make_paginator(self, pages):
        """Return a mock paginator that yields the given list of page dicts."""
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = iter(pages)
        return mock_paginator

    def test_returns_objects_from_all_pages(self):
        """list_objects must collect results across multiple paginator pages."""
        svc = _service()
        page1 = {"Contents": [{"Key": "satellite-images/a.jpg", "Size": 100, "StorageClass": "STANDARD"}]}
        page2 = {"Contents": [{"Key": "satellite-images/b.jpg", "Size": 200, "StorageClass": "GLACIER"}]}

        mock_client = MagicMock()
        mock_client.get_paginator.return_value = self._make_paginator([page1, page2])
        svc._client = mock_client

        result = svc.list_objects(prefix="satellite-images/")

        assert result["success"] is True
        assert result["count"] == 2
        assert result["bucket"] == "test-bucket"
        assert result["prefix"] == "satellite-images/"
        keys = [o["key"] for o in result["objects"]]
        assert "satellite-images/a.jpg" in keys
        assert "satellite-images/b.jpg" in keys

    def test_empty_bucket_returns_zero_count(self):
        """An empty page (no Contents key) must yield count=0, not an error."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = self._make_paginator([{}])
        svc._client = mock_client

        result = svc.list_objects()

        assert result["success"] is True
        assert result["count"] == 0
        assert result["objects"] == []

    def test_custom_prefix_is_forwarded(self):
        """list_objects must pass the caller-supplied prefix to paginate()."""
        svc = _service()
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = iter([{}])
        mock_client.get_paginator.return_value = mock_paginator
        svc._client = mock_client

        svc.list_objects(prefix="archive/2026/")

        mock_paginator.paginate.assert_called_once_with(
            Bucket="test-bucket", Prefix="archive/2026/"
        )

    def test_client_error_returns_failure(self):
        """ClientError during list must yield success=False with safe message."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _make_client_error(
            "NoSuchBucket", "The specified bucket does not exist"
        )
        svc._client = mock_client

        result = svc.list_objects()

        assert result["success"] is False
        assert "NoSuchBucket" in result["error"] or "does not exist" in result["error"]
        assert result["bucket"] == "test-bucket"

    def test_object_fields_are_present(self):
        """Each returned object dict must contain key, size_bytes, storage_class."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = self._make_paginator([{
            "Contents": [{"Key": "satellite-images/x.jpg", "Size": 512, "StorageClass": "STANDARD_IA"}]
        }])
        svc._client = mock_client

        result = svc.list_objects()
        obj = result["objects"][0]

        assert obj["key"] == "satellite-images/x.jpg"
        assert obj["size_bytes"] == 512
        assert obj["storage_class"] == "STANDARD_IA"


# ---------------------------------------------------------------------------
# head_object
# ---------------------------------------------------------------------------

class TestHeadObject:

    def test_existing_object_returns_exists_true(self):
        """A successful HeadObject response must set exists=True with size and class."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.head_object.return_value = {
            "ContentLength": 2048,
            "StorageClass": "GLACIER",
        }
        svc._client = mock_client

        result = svc.head_object("satellite-images/img.jpg")

        assert result["exists"] is True
        assert result["size_bytes"] == 2048
        assert result["storage_class"] == "GLACIER"
        assert result["object_key"] == "satellite-images/img.jpg"
        assert result["bucket"] == "test-bucket"

    def test_404_returns_exists_false_no_error_key(self):
        """A 404 ClientError must yield exists=False without an 'error' key."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.head_object.side_effect = _make_client_error("404", "Not Found")
        svc._client = mock_client

        result = svc.head_object("satellite-images/missing.jpg")

        assert result["exists"] is False
        assert "error" not in result

    def test_no_such_key_error_returns_exists_false(self):
        """NoSuchKey ClientError must also yield exists=False without 'error' key."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.head_object.side_effect = _make_client_error("NoSuchKey")
        svc._client = mock_client

        result = svc.head_object("satellite-images/ghost.jpg")

        assert result["exists"] is False
        assert "error" not in result

    def test_access_denied_returns_exists_false_with_error(self):
        """Non-404 ClientErrors must surface exists=False with a safe error message."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.head_object.side_effect = _make_client_error(
            "AccessDenied", "Access Denied"
        )
        svc._client = mock_client

        result = svc.head_object("satellite-images/private.jpg")

        assert result["exists"] is False
        assert "error" in result
        assert "AccessDenied" in result["error"] or "Access Denied" in result["error"]

    def test_object_key_and_bucket_always_present(self):
        """bucket and object_key must be present in every head_object response."""
        svc = _service()
        mock_client = MagicMock()
        mock_client.head_object.side_effect = _make_client_error("404")
        svc._client = mock_client

        result = svc.head_object("some/key.jpg")

        assert result["bucket"] == "test-bucket"
        assert result["object_key"] == "some/key.jpg"


# ---------------------------------------------------------------------------
# Client construction (profile / credential handling)
# ---------------------------------------------------------------------------

class TestClientConstruction:

    @patch("web.services.s3_service.boto3.Session")
    def test_profile_passed_to_session_when_set(self, mock_session_cls):
        """When AWS_PROFILE / profile is set, it must be forwarded to boto3.Session."""
        mock_session = MagicMock()
        mock_session.client.return_value = MagicMock()
        mock_session_cls.return_value = mock_session

        svc = S3Service(bucket="b", region="us-east-1", profile="intelliarchive")
        svc._get_client()

        mock_session_cls.assert_called_once_with(
            region_name="us-east-1", profile_name="intelliarchive"
        )

    @patch("web.services.s3_service.boto3.Session")
    def test_no_profile_kwarg_when_profile_is_empty(self, mock_session_cls):
        """When profile is empty, profile_name must NOT be passed to boto3.Session."""
        mock_session = MagicMock()
        mock_session.client.return_value = MagicMock()
        mock_session_cls.return_value = mock_session

        svc = S3Service(bucket="b", region="us-east-1", profile="")
        svc._get_client()

        call_kwargs = mock_session_cls.call_args[1]
        assert "profile_name" not in call_kwargs

    @patch("web.services.s3_service.boto3.Session")
    def test_client_is_cached_after_first_call(self, mock_session_cls):
        """_get_client must not create a new Session on subsequent calls."""
        mock_session = MagicMock()
        mock_session.client.return_value = MagicMock()
        mock_session_cls.return_value = mock_session

        svc = S3Service(bucket="b", region="us-east-1", profile="")
        c1 = svc._get_client()
        c2 = svc._get_client()

        assert c1 is c2
        mock_session_cls.assert_called_once()

    def test_default_bucket_and_region_from_module_constants(self):
        """A no-arg S3Service must use the module-level defaults."""
        import web.services.s3_service as mod
        svc = S3Service()
        assert svc.bucket == mod.BUCKET_NAME
        assert svc.region == mod.AWS_REGION
