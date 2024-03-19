"""
Utils Module
"""

from datetime import datetime, timezone
from http import HTTPStatus

import argon2
from flask import Response, jsonify

from app.enums import Argon2IdHash
from app.settings import SECRET_SALT_KEY


def argon2id_hasher(data: bytes) -> bytes:
    """
    Function to hash data using argon2id hashing.

    Args:
        data (bytes): Data to hash

    Returns:
        bytes: Hashed data.
    """

    return argon2.hash_password_raw(
        time_cost=Argon2IdHash.TIME_COST.value,
        memory_cost=Argon2IdHash.MEMORY_COST.value,
        parallelism=Argon2IdHash.PARALLELISM.value,
        hash_len=Argon2IdHash.HASH_LENGTH.value,
        password=data,
        salt=SECRET_SALT_KEY.encode(),
        type=argon2.low_level.Type.ID,
    )


def make_response(
    message: str,
    data: dict = None,
    errors: dict = None,
    status_code: HTTPStatus = HTTPStatus.OK
) -> tuple[Response, HTTPStatus]:
    """
    Function to make response.

    Args:
        message (str): Response message.
        data (dict, optional): Response data. Defaults to None.
        errors (dict, optional): Error details. Defaults to None.
        status_code (HTTPStatus, optional): Response status code. Defaults to HTTPStatus.OK.

    Returns:
        tuple[Response, HTTPStatus]: Response and status code.
    """

    response = {"message": message, "data": data or {}}
    if errors:
        response.update(errors)
    return jsonify(response), status_code


def get_current_datetime() -> datetime:
    """
    Function to get current datetime in utc timezone.

    Returns:
        datetime: Current datetime in utc timezone.
    """

    return datetime.now(timezone.utc)
