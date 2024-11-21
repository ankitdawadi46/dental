from rest_framework.response import Response

class BaseResponse(Response):
    def __init__(self, data=None, status=None, message=None):
        """
        Custom response class to provide a standard structure.
        
        Args:
            data (dict or list, optional): The actual response data.
            status (str, optional): A string representing the status (e.g., 'success' or 'error').
            message (str, optional): A message describing the result (e.g., "Data retrieved successfully").
        """
        # Default values if no data or message is passed
        if data is None:
            data = {}
        if message is None:
            message = "Request processed successfully"
        if status is None:
            status = 200

        # Standardized response format
        response_data = {
            "status": status,
            "message": message,
            "data": data
        }

        super().__init__(response_data, status=status)
