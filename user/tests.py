import pytest
from rest_framework.reverse import reverse

from user.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user(username='pooja123', email='puja@gmail.com', phone=123456789, location='delhi',
                             password='12345678')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_login_api_with_invalid_credentials(client):
    url = reverse('log_in')
    data = {'username': 'pooja@123', 'password': 'test@123'}
    response = client.post(url, data, content_type='application/json')
    print(response.data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_as_login_successfully(client):
    # Create user
    User.objects.create_user(username='pooja', email='puja@gmail.com', phone=123456789, location='delhi',
                             password='test@123',is_verify=True)
    url = reverse('log_in')
    data = {'username': 'pooja', 'password': 'test@123'}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.data['message'] == 'Login Success'


@pytest.mark.django_db
def test_response_as_registration_successfully(client):
    url = reverse('register_api')
    data = {'username': 'pooja', 'email': 'pooja@gmail.com', 'phone': '123456789', 'location': 'delhi',
            'password': 'test@123'}
    response = client.post(url, data, format='json', content_type="application/json")
    assert response.status_code == 200



@pytest.mark.django_db
def test_registration_with_invalid_details(client):
    url = reverse('register_api')
    data = {'email': 'puja@gmail.com', 'phone': '123455678',
            'password': 'test@123'}
    response = client.post(url, data, format='json', content_type="application/json")
    assert response.status_code == 400
