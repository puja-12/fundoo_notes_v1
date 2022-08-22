from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
import logging
from user.models import  User

# Create your views here.

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login

logger = logging.getLogger('django')


@csrf_exempt
def register_api(request):
    """
    post method for registering a user
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = User.objects.create_user(**data)
            print(user)
            logger.info("User successfully Registered ")

            return JsonResponse({'message': f"{user.username} Register successfully"})
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
            username = data.get('username')
            password = data.get('password')
            user = authenticate( username=username, password=password)

            if user is not None:

                logger.info("User is successfully logged in")
                return JsonResponse({'success': True, 'message': 'Login Success'})

            return JsonResponse({'success': False, 'message': 'Login failed!'})

        except Exception as e:
            logger.exception(e)
            return JsonResponse({'success': False, 'message': 'Login failed!, Something Went Wrong',
                                 'data': str(e)})



