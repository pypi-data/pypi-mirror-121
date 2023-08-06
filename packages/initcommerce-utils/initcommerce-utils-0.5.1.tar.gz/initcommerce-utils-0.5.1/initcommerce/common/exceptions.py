import abc
import re

from graphql import GraphQLError


class InitCommerceBaseException(GraphQLError, metaclass=abc.ABCMeta):
    path = None
    locations = ""
    original_error = None
    extensions = None
    _message: str = None

    def __init__(self, message=None):
        self._message = message

    @property
    def message(self):
        if self._message is not None:
            return self._message.replace(" ", "_").upper()

        class_name = self.__class__.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).upper()
