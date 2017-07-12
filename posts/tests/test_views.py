import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import RequestFactory
from mixer.backend.django import mixer
from posts.views import draft_page, index_page, post_create, post_detail

# To disable mixer from writting data into DB
pytestmark = pytest.mark.django_db


class TestIndexPage:
    # To check whether index page is accessible for public
    def test_anonymous(self):
        # Creating a fake "GET" request to / through RequestFactory
        request = RequestFactory().get("/")
        response = index_page(request)
        assert response.status_code == 200, 'Index Page should be accessible to everyone'


class TestDraftPage:
    # To check whether Draft page is accessible for public
    def test_anonymous(self):
        # Creating a fake "GET" request to /drafts/ through RequestFactory
        request = RequestFactory().get("/drafts/")
        # AnonymousUser() will allow us to create a user which is not in the DB
        request.user = AnonymousUser()
        with pytest.raises(Http404) as e:
            draft_page(request)
        assert "404" in str(e), 'Draft Page should not be accessible to public'

    # To check whether Draft page is accessible for public
    def test_admin(self):
        # Creating a dummy super from auth.User table
        user = mixer.blend("auth.User", is_superuser = True)
        request = RequestFactory().get("/drafts/")
        request.user = user
        response = draft_page(request)
        assert response.status_code == 200, 'Draft Page should be accessible to admin'


class TestPostCreate:
    # To check whether Post create page is accessible for public
    def test_anonymous(self):
        # Creating a fake "GET" request to /create/ through RequestFactory
        request = RequestFactory().get("/create/")
        # AnonymousUser() will allow us to create a user which is not in the DB
        request.user = AnonymousUser()
        with pytest.raises(Http404) as e:
            post_create(request)
        assert "404" in str(e), 'Post create page should not be accessible to public'

    # To check whether Post create page is accessible for public
    def test_admin(self):
        # Creating a dummy super from auth.User table
        user = mixer.blend("auth.User", is_superuser = True)
        request = RequestFactory().get("/create/")
        request.user = user
        response = post_create(request)
        assert response.status_code == 200, 'Post create page should be accessible to admin'
