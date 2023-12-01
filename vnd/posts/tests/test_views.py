import json

import pytest
from model_bakery import baker
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from api.models import Tag
from posts.models import Category, Post
from users.models import CustomUser


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return baker.make(CustomUser)


@pytest.fixture
def categories():
    return baker.make(Category, _quantity=5)


@pytest.fixture
def posts(categories, user):
    tag = baker.make(Tag)
    return baker.make(Post, _quantity=10, make_m2m=True, categories=[cat for cat in categories], authors=[user],
                      tags=[tag])


@pytest.mark.django_db
class TestCategories:
    @pytest.fixture(autouse=True)
    def setup(self, client, user, categories):
        self.client = client
        self.user = user
        self.categories = categories

    def test_get(self):
        category = self.categories[0]
        response = self.client.get("/api/v1/posts/categories/")
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 5
        response = self.client.get(f"/api/v1/posts/categories/{category.id}/")
        assert response.status_code == HTTP_200_OK

    def test_permissions(self):
        args = ["/api/v1/posts/categories/", {"name": "biography"}]
        response = self.client.post(*args)
        assert response.status_code == 401
        self.client.force_authenticate(self.user)
        response = self.client.post(*args)
        assert response.status_code == 403
        response = self.client.delete(*args)
        assert response.status_code == 403

    def test_post(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/v1/posts/categories/", {"name": "biography"})
        assert response.status_code == 201
        assert response.data["name"] == "biography"

    def test_delete(self):
        self.user.is_staff = True
        self.user.save()
        category = self.categories[0]
        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/v1/posts/categories/{category.id}/")
        assert response.status_code == 204
        response = self.client.get("/api/v1/posts/categories/")
        assert len(response.data) == 4


@pytest.mark.django_db
class TestPosts:
    @pytest.fixture(autouse=True)
    def setup(self, client, categories, user, posts):
        self.client = client
        self.categories = categories
        self.user = user
        self.post = posts[0]

    def test_permission(self):
        path = "/api/v1/posts/"
        response = self.client.post(path, format="json")
        assert response.status_code == 401
        random_user = baker.make(CustomUser)
        self.client.force_authenticate(random_user)
        response = self.client.put(f"{path}{self.post.id}/", format="json")
        assert response.status_code == 403

    def test_post(self):
        rich_text = """<p>Wow, this editor instance exports its content as HTML.</p><p><strong>Bold  text</strong></p><p></p><p><strong><em>Bold Italick</em></strong></p><p></p>"""
        author = self.user
        tag = baker.make(Tag)
        args = ["/api/v1/posts/",
                {"title": "Title", "body": rich_text, "categories": [cat.id for cat in self.categories],
                 "authors": author.id, "tags": tag.id}]
        self.client.force_authenticate(self.user)
        response = self.client.post(*args)
        assert response.status_code == 201
        assert response.data["body"] == rich_text
        args[1]["body"] += "<script></script>"
        response = self.client.post(*args)
        assert response.data["body"] == rich_text

    def test_update(self, posts, user):
        args = [f"/api/v1/posts/{posts[0].id}/", {"categories": self.categories[0].id}]
        prev_categories = [cat.id for cat in posts[0].categories.all()]
        response = self.client.patch(*args)
        assert response.status_code == 401
        response = self.client.put(*args)
        assert response.status_code == 401
        self.client.force_authenticate(user)
        response = self.client.patch(*args)
        assert response.status_code == 200
        assert response.data["categories"] != prev_categories

    def test_relations(self):
        response = self.client.get("/api/v1/posts/")
        assert response.data[0]["relation"] == {"like": False, "bookmark": False}
        self.client.force_authenticate(self.user)
        response = self.client.post(f"/api/v1/posts/{self.post.pk}/set_relation/",
                                    json.dumps({"like": False, "bookmark": True}), content_type="application/json")
        assert response.data == {"like": False, "bookmark": True}
        response = self.client.post(f"/api/v1/posts/{self.post.pk}/set_relation/", json.dumps({"like": False}),
                                    content_type="application/json")
        assert response.data == {"like": False, "bookmark": True} == \
               self.client.get(f"/api/v1/posts/{self.post.pk}/").data["relation"]
