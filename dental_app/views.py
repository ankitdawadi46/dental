from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def error_api(request):
    if request.method == "GET":
        # Handle GET requests
        data = {"message": "Hello, this is a GET request!"}
        return JsonResponse(data, status=200)

    elif request.method == "POST":
        # Handle POST requests
        try:
            body = json.loads(request.body)  # Parse JSON body
            name = body.get("name", "Guest")
            data = {"message": f"Hello, {name}! This is a POST request!"}
            return JsonResponse(data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Method not allowed
    return JsonResponse({"error": "Method not allowed"}, status=405)