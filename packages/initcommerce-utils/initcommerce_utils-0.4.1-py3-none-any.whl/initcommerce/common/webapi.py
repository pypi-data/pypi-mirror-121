from functools import partial

import graphene as graphql
import uvicorn as WebServer
from fastapi import APIRouter as Router
from fastapi import Body
from fastapi import FastAPI as WebApp
from starlette_graphene3 import GraphQLApp as _GraphQLApp
from starlette_graphene3 import format_error as _format_error
from starlette_graphene3 import make_graphiql_handler

from .exceptions import InitCommerceBaseException
from .logger import get_logger

logger = get_logger(__name__)


def _error_formatter(err):
    if isinstance(err, InitCommerceBaseException):
        return _format_error(err)
    logger.critical(err)
    return _format_error(InitCommerceBaseException("INTERNAL_SERVER_ERROR"))


GraphQLApp: _GraphQLApp = partial(_GraphQLApp, error_formatter=_error_formatter)


__all__ = [
    Body,
    graphql,
    GraphQLApp,
    make_graphiql_handler,
    Router,
    WebApp,
    WebServer,
]
