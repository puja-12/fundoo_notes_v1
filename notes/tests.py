import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_post_user_with_success_response( client, django_user_model, authentication_user):

    user_id = authentication_user
    url = reverse("notedetails")
    data = {"title": "tea", "description": "famous in india", "user": user_id}
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
