from rest_framework_simplejwt.tokens import AccessToken
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from users.models import CustomUser

client = APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "123wedsadweq"
    }


@pytest.fixture
def user():
    user = CustomUser.objects.create_user(username="testuser", password="123wedsadweq")
    return user


@pytest.fixture
def token(user):
    return str(AccessToken.for_user(user))


@pytest.mark.django_db
class TestAuthentication:
    def test_user_registration(self, user_data):
        path = "/api/v1/users/register/"
        response = client.post(path, user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.data
        assert CustomUser.objects.count() == 1

    def test_user_login(self, user):
        path = "/api/v1/users/login/"
        response = client.post(path, {"username": "testuser", "password": "123wedsadweq"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "username" in response.data


@pytest.mark.django_db
class TestUsersViews:
    def test_user_list(self, user):
        path = "/api/v1/users/"
        response = client.get(path)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["username"] == "testuser"

    def test_user_detail(self, user, token):
        path = "/api/v1/users/detail/"
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = client.get(path)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "testuser"
        response = client.delete(path)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CustomUser.objects.count() == 0


