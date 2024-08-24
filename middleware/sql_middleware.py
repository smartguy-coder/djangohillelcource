import time
import logging
import datetime as dt

from django.db import connection

logger = logging.getLogger(__name__)


class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Перед виконанням запиту
        start_queries = len(connection.queries)
        start_time = time.time()

        response = self.get_response(request)

        # Після виконання запиту
        end_queries = len(connection.queries)
        total_queries = end_queries - start_queries
        total_time = time.time() - start_time

        logger.debug(
            f"[->] {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {total_queries}"
            f" queries executed in {total_time:.2f} seconds for path: {request.path}")
        return response





