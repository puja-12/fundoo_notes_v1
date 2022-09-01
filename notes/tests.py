import json
from notes.models import Notes
import pytest
from rest_framework.reverse import reverse


pytestmark = pytest.mark.django_db



@pytest.fixture
def authentication_user(client, django_user_model, db):
    """
    creating user id for note app crud operation testing
    :param client:
    :param django_user_model:
    :return:
    """
    user = django_user_model.objects.create_user(username='pooja123', email='puja@gmail.com', phone=123456789,
                                                 location='delhi',
                                                 password='12345678',is_verify=True)
    url = reverse('log_in')
    data = {'username': 'pooja123', 'password': '12345678'}
    response = client.post(url, data)
    print(response.data)
    token = response.data.get('data').get('token_key')
    return token, user.id



@pytest.mark.django_db
def test_post_user_with_success_response(client, authentication_user):
    """
   Test post api
   :param client:
   :param django_user_model:
   :param authentication_user:
   :return:
    """
    token,user_id = authentication_user
    url = reverse("note_api")
    data = {"title": "Django", "description": "framework", "user": user_id,}
    response = client.post(url, data, content_type='application/json', HTTP_TOKEN=token)
    assert response.status_code == 201

@pytest.mark.django_db
def test_note_put_api_response(client, authentication_user):
    """
      Test put api
      :param client:
      :param authentication_user:
      :return:
    """
    token, user_id = authentication_user

    # create note
    url = reverse("note_api")
    data = {"title": "Django", "description": "framework", "user": user_id}
    response = client.post(url, data, content_type='application/json', HTTP_TOKEN=token)
    json_data = json.loads(response.content)
    assert response.status_code == 201
    note_id = json_data.get('data').get('id')
    # update note
    url = reverse("note_api")
    data = {"id": note_id, "title": "Fruit", "description": "Apple", "user": user_id,}
    response = client.put(url, data, content_type='application/json',HTTP_TOKEN=token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_note_get_api_response(client, authentication_user):
    """
   Test get api
   :param client:
   :param authentication_user:
   :return:
   """
    token,user_id = authentication_user
    # create note
    url = reverse("note_api")
    data = {"title": "Fruit", "description": "Apple", "user": user_id}
    response = client.post(url, data, content_type='application/json',HTTP_TOKEN=token)
    assert response.status_code == 201
    # get note
    url = reverse('note_api')
    response = client.get(url, content_type='application/json',HTTP_TOKEN=token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_note_delete_response(client, authentication_user):
    """
   Test delete api
   :param client:
   :param authentication_user:
   :return:
   """
    token,user_id = authentication_user
    # new note
    url = reverse('note_api')
    data = {'title': 'Django', 'description': 'framework', "user": user_id}
    response = client.post(url, data, content_type='application/json',HTTP_TOKEN=token)
    json_data = json.loads(response.content)
    assert response.status_code == 201
    print(response)
    note_id = json_data.get('data').get('id')
    # Delete notes
    url = reverse("note_api")
    data = {'id': note_id}
    response = client.delete(url, data, content_type='application/json',HTTP_TOKEN=token)
    assert response.status_code == 200
    assert response.data['message'] == 'Notes deleted successfully'