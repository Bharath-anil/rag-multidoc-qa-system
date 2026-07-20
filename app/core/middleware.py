import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        end = time.time()
        duration = end - start

        client_host = request.client.host if request.client else "unknown"
        logger.info(
            f"{client_host} | "
            f"{request.method} | "
            f"{request.url.path} | "
            f"{response.status_code} | "
            f"{duration:.2f} ms"
        )

        return response