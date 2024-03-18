"""
Main Module
"""

from http import HTTPStatus

from flask import Response

from app.settings import LIMITER

@LIMITER.limit("100/hour;10/minute")
def signup() -> tuple[Response, HTTPStatus]:
    return "Success", HTTPStatus.OK
