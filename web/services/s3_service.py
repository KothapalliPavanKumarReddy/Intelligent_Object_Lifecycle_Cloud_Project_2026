"""
web/services/s3_service.py
==========================
AWS S3 client wrapper for IntelliArchive.

Configuration is read exclusively from environment variables so that no
credentials or secrets are ever present in source code.

Environment variables
---------------------
INTELLIARCHIVE_S3_BUCKET
    Target S3 bucket.  Defaults to ``intelliarchive-pavan-satellite-2026``.
AWS_REGION
    AWS region.  Defaults to ``ap-south-1``.
AWS_PROFILE
    Named AWS credentials profile to use when the application runs locally.
    Defaults to ``intelliarchive``.  Set this to an empty string (``""``) to
    skip profile-based authentication (e.g. when running inside an EC2 instance
    that uses an attached IAM role instead).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound

# ---------------------------------------------------------------------------
# Module-level configuration (read once at import time)
# ---------------------------------------------------------------------------

#: S3 bucket where satellite imagery is stored.
BUCKET_NAME: str = os.environ.get(
    "INTELLIARCHIVE_S3_BUCKET",
    "intelliarchive-pavan-satellite-2026",
)

#: AWS region that hosts the bucket.
AWS_REGION: str = os.environ.get("AWS_REGION", "ap-south-1")

#: Named credentials profile used for local development.
#: Defaults to "intelliarchive" when unset. If AWS_PROFILE is set but empty or whitespace,
#: it is purged from os.environ and resolved to None so that botocore/boto3 defaults
#: to standard credential chains (such as ECS Task Roles) without raising ProfileNotFound.
_env_profile: Optional[str] = os.environ.get("AWS_PROFILE")
if _env_profile is not None:
    if not _env_profile.strip():
        os.environ.pop("AWS_PROFILE", None)
        AWS_PROFILE: Optional[str] = None
    else:
        AWS_PROFILE = _env_profile.strip()
else:
    # AWS_PROFILE is unset: preserve local development default
    AWS_PROFILE = "intelliarchive"


# ---------------------------------------------------------------------------
# Service class
# ---------------------------------------------------------------------------

class S3Service:
    """
    Thin wrapper around the boto3 S3 client.

    The client is created lazily on first use so that importing this module
    never fails even when boto3 is absent from the environment (tests can
    mock it before the client is instantiated).

    Credentials are **never** hardcoded here.  Authentication priority:

    1. Named profile set via ``AWS_PROFILE`` (local dev).
    2. Standard boto3 credential chain: env vars → ~/.aws/credentials →
       IAM instance/task role (production).
    """

    def __init__(
        self,
        bucket: Optional[str] = None,
        region: Optional[str] = None,
        profile: Optional[str] = None,
    ) -> None:
        self.bucket: str = bucket or BUCKET_NAME
        self.region: str = region or AWS_REGION
        resolved_profile = profile if profile is not None else AWS_PROFILE
        self._profile: Optional[str] = (
            resolved_profile.strip() if resolved_profile and resolved_profile.strip() else None
        )
        self._client: Optional[Any] = None  # created lazily

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_client(self) -> Any:
        """Return (and cache) the boto3 S3 client."""
        if self._client is None:
            # Defensive check: if AWS_PROFILE in os.environ is empty/whitespace, remove it
            # so botocore internal configuration loaders do not fail with ProfileNotFound.
            current_env_profile = os.environ.get("AWS_PROFILE")
            if current_env_profile is not None and not current_env_profile.strip():
                os.environ.pop("AWS_PROFILE", None)

            session_kwargs: Dict[str, Any] = {"region_name": self.region}
            if self._profile and self._profile.strip():
                try:
                    session = boto3.Session(profile_name=self._profile.strip(), **session_kwargs)
                    self._client = session.client("s3")
                    return self._client
                except ProfileNotFound:
                    # Named profile does not exist in this environment (e.g. AWS EC2/ECS/Docker).
                    # Fall back to default credential provider chain (IAM instance role / env vars).
                    self._profile = None

            session = boto3.Session(**session_kwargs)
            self._client = session.client("s3")
        return self._client

    @staticmethod
    def _safe_error_message(exc: Exception) -> str:
        """
        Extract a user-friendly error string from an Exception without
        leaking any credential or secret information.
        """
        if isinstance(exc, ClientError):
            code = exc.response.get("Error", {}).get("Code", "UnknownError")
            message = exc.response.get("Error", {}).get("Message", str(exc))
            return f"AWS S3 error [{code}]: {message}"
        return f"AWS S3 error: {type(exc).__name__} - {str(exc)}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def upload_file(
        self,
        file_path: str | Path,
        object_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a local file to the configured S3 bucket.

        Parameters
        ----------
        file_path:
            Absolute or relative path to the local file.
        object_key:
            S3 object key (path inside the bucket).  When omitted, the
            file's basename is used under the ``satellite-images/`` prefix.

        Returns
        -------
        dict
            On success::

                {
                    "success": True,
                    "bucket": "<bucket>",
                    "object_key": "<key>",
                    "local_path": "<file_path>",
                    "region": "<region>",
                }

            On failure::

                {
                    "success": False,
                    "error": "<human-readable message>",
                    "local_path": "<file_path>",
                }
        """
        file_path = Path(file_path)
        if object_key is None:
            object_key = f"satellite-images/{file_path.name}"

        try:
            self._get_client().upload_file(
                Filename=str(file_path),
                Bucket=self.bucket,
                Key=object_key,
            )
            return {
                "success": True,
                "bucket": self.bucket,
                "object_key": object_key,
                "local_path": str(file_path),
                "region": self.region,
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"Local file not found: '{file_path}'",
                "local_path": str(file_path),
            }
        except (ClientError, BotoCoreError, Exception) as exc:
            return {
                "success": False,
                "error": self._safe_error_message(exc),
                "local_path": str(file_path),
            }

    def list_objects(self, prefix: str = "satellite-images/") -> Dict[str, Any]:
        """
        List objects in the configured bucket under *prefix*.

        Parameters
        ----------
        prefix:
            S3 key prefix to filter results.

        Returns
        -------
        dict
            On success::

                {
                    "success": True,
                    "bucket": "<bucket>",
                    "prefix": "<prefix>",
                    "objects": [
                        {"key": "<key>", "size_bytes": <int>, "storage_class": "<class>"},
                        ...
                    ],
                    "count": <int>,
                }

            On failure::

                {
                    "success": False,
                    "error": "<human-readable message>",
                    "bucket": "<bucket>",
                    "prefix": "<prefix>",
                }
        """
        try:
            paginator = self._get_client().get_paginator("list_objects_v2")
            objects = []
            for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                for obj in page.get("Contents", []):
                    objects.append(
                        {
                            "key": obj["Key"],
                            "size_bytes": obj["Size"],
                            "storage_class": obj.get("StorageClass", "STANDARD"),
                        }
                    )
            return {
                "success": True,
                "bucket": self.bucket,
                "prefix": prefix,
                "objects": objects,
                "count": len(objects),
            }
        except (ClientError, BotoCoreError, Exception) as exc:
            return {
                "success": False,
                "error": self._safe_error_message(exc),
                "bucket": self.bucket,
                "prefix": prefix,
            }

    def head_object(self, object_key: str) -> Dict[str, Any]:
        """
        Check whether an object exists in the bucket and return its metadata.

        Parameters
        ----------
        object_key:
            Full S3 object key.

        Returns
        -------
        dict
            When the object exists::

                {
                    "exists": True,
                    "bucket": "<bucket>",
                    "object_key": "<key>",
                    "size_bytes": <int>,
                    "storage_class": "<class>",
                }

            When the object does not exist (HTTP 404 / NoSuchKey)::

                {
                    "exists": False,
                    "bucket": "<bucket>",
                    "object_key": "<key>",
                }

            On any other AWS error::

                {
                    "exists": False,
                    "bucket": "<bucket>",
                    "object_key": "<key>",
                    "error": "<human-readable message>",
                }
        """
        try:
            response = self._get_client().head_object(
                Bucket=self.bucket, Key=object_key
            )
            return {
                "exists": True,
                "bucket": self.bucket,
                "object_key": object_key,
                "size_bytes": response.get("ContentLength", 0),
                "storage_class": response.get("StorageClass", "STANDARD"),
            }
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in ("404", "NoSuchKey"):
                return {
                    "exists": False,
                    "bucket": self.bucket,
                    "object_key": object_key,
                }
            return {
                "exists": False,
                "bucket": self.bucket,
                "object_key": object_key,
                "error": self._safe_error_message(exc),
            }
        except (BotoCoreError, Exception) as exc:
            return {
                "exists": False,
                "bucket": self.bucket,
                "object_key": object_key,
                "error": self._safe_error_message(exc),
            }


# ---------------------------------------------------------------------------
# Module-level singleton (lazy — client not created until first call)
# ---------------------------------------------------------------------------

#: Pre-configured singleton for use throughout the application.
s3_service = S3Service()
