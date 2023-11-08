from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework_simplejwt.tokens import AccessToken
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from users.models import CustomUser, Engine, Status


@pytest.fixture
def client():
    return APIClient()


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


@pytest.fixture
def engine():
    return Engine.objects.create(name="Test", links={"test": "test"}, description="dsadsafeqwas")


@pytest.fixture
def status():
    return Status.objects.create(name="Test")


@pytest.mark.django_db
class TestAuthentication:
    def test_user_registration(self, user_data, client):
        path = "/api/v1/users/register/"
        response = client.post(path, user_data, format="json")
        assert response.status_code == HTTP_201_CREATED
        assert "password" not in response.data
        assert CustomUser.objects.count() == 1

    def test_user_login(self, user, client):
        path = "/api/v1/users/login/"
        response = client.post(path, {"username": "testuser", "password": "123wedsadweq"}, format="json")
        assert response.status_code == HTTP_200_OK
        assert "access", "refresh" in response.data


@pytest.mark.django_db
class TestUsersViews:
    def test_user_list(self, user, client):
        path = "/api/v1/users/"
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        assert response.data[0]["username"] == "testuser"

    def test_user_detail(self, user, token, client):
        path = "/api/v1/users/detail/"
        response = client.get(path)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        assert response.data["username"] == "testuser"
        response = client.delete(path)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert CustomUser.objects.count() == 0


@pytest.mark.django_db
class TestPermissions:

    def test_get(self, engine, client):
        path = "/api/v1/"
        response = client.get(path + "engines/")
        assert response.status_code == HTTP_200_OK
        response = client.get(path + "statuses/")
        assert response.status_code == HTTP_200_OK

    def test_create(self, client):
        path = "/api/v1/"
        response = client.post(path + "engines/")
        assert response.status_code == HTTP_401_UNAUTHORIZED
        response = client.post(path + "statuses/")
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_delete(self, engine, status, client):
        path = "/api/v1/"
        response = client.delete(path + f"engines/{engine.id}/")
        assert response.status_code == HTTP_401_UNAUTHORIZED
        response = client.delete(path + f"engines/{id}/")
        assert response.status_code == HTTP_401_UNAUTHORIZED
