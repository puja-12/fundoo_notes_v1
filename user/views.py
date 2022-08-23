import json
import logging

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from user.serializers import RegisterSerializer

# Create your views here.


logger = logging.getLogger('django')
@csrf_exempt
def register_api(request):
    """
    post method for registering a user
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info("User successfully Registered ")
                return JsonResponse({'message': 'Register successfully'})
            return JsonResponse({'message': 'invalid details'}, serializer.errors)

        except Exception as e:
            logger.exception(e)
            return JsonResponse({'message': 'invalid details'})


@csrf_exempt
def log_in(request):
    """
     post method for checking login operation
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = authenticate(**data)
            if user:
                logger.info("User is successfully logged in")
                return JsonResponse({'success': True, 'message': 'Login Success'})

            return JsonResponse({'success': False, 'message': 'Invalid credentials used!'})

        except Exception as e:
            logger.exception(e)
            return JsonResponse({'success': False, 'message': 'Login failed!, Something Went Wrong',
                                 'data': str(e)})
