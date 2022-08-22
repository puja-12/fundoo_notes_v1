from django.http import JsonResponse
import json
import logging

# Create your views here.

from django.views.decorators.csrf import csrf_exempt

from user.models import User
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

            register = User.objects.create(first_name=data.get('first_name'),
                                           last_name=data.get('last_name'),
                                           password=data.get('password'), phone=data.get('phone'),
                                           email=data.get('email'), location=data.get('location'))
            print(register)
            logger.info("User successfully Registered ")

            return JsonResponse({'message': 'Register successfully'})
        except Exception as e:
            logger.exception(e)
            return JsonResponse({'message': 'not done'})


@csrf_exempt
def log_in(request):
    """
     post method for checking login operation
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get['email']
            password = data.get['password']
            user_list = User.objects.filter(email=email, password=password)
            if user_list.exists():
                login(request, user_list.first())
                logger.info("User is successfully logged in")
                return JsonResponse({'success': True, 'message': 'Login Success'})

            return JsonResponse({'success': False, 'message': 'Login failed!'})

        except Exception as e:
            logger.exception(e)
            return JsonResponse({'success': False, 'message': 'Login failed!, Something Went Wrong',
                                 'data': str(e)})
