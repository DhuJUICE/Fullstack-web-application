import time
import logging

logger = logging.getLogger('rest_API.performance')

class PerformanceLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.error_count = 0  # Initialize error count

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
        
        # Check for errors and log them
        if response.status_code >= 400:  # Error codes (4xx or 5xx)
            self.error_count += 1
            logger.error(
                f"Error: Method: {request.method}, Path: {request.path}, "
                f"Status: {response.status_code}, Duration: {duration:.2f} seconds"
            )
        
        return response