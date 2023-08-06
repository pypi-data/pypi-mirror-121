from logging import getLogger

import warnings
from asgiref.sync import sync_to_async

from momotor.shared.log import async_log_exception, log_exception

__all__ = ['AsyncLogWrapper', 'getAsyncLogger', 'async_log_exception', 'log_exception']

warnings.warn('momotor.django.log module is deprecated; use momotor.shared.log instead', DeprecationWarning)


class AsyncLogWrapper:
    def __init__(self, logger):
        self._logger = logger

    def __getattr__(self, item):
        attr = getattr(self._logger, item)
        if callable(attr):
            attr = sync_to_async(attr, thread_sensitive=True)

        setattr(self, item, attr)
        return attr


# noinspection PyPep8Naming
def getAsyncLogger(name):
    return AsyncLogWrapper(getLogger(name))
