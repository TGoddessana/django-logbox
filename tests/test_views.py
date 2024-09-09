import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_temp_view():
    client = Client()
    response = client.get(reverse('temp_view'))
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}