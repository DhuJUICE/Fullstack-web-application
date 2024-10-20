import time
import logging

logger = logging.getLogger(__name__)

class PerformanceLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start time
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log performance metrics
        logger.info(
            f"Method: {request.method}, Path: {request.path}, "
            f"Status: {response.status_code}, Duration: {duration:.2f} seconds"
        )
        
        return response
