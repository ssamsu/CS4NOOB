import pytest
from mixer.backend.django import mixer
from posts.models import Category, Feedback, Post

# To disable mixer from writting data into DB
pytestmark = pytest.mark.django_db


class TestPost:
    # To check whether Post instance can be created and saved
    def test_init(self):
        obj = mixer.blend(Post)
        assert obj.pk == 1, 'Should save an Post instance'

    # To check whether Post instance returns proper title string
    def test_str(self):
        obj = mixer.blend(Post, title = "Post title")
        assert str(obj) == "Post title", 'Post instance __str__() should return title'


class TestFeedback:
    # To check whether Feedback instance can be created and saved
    def test_init(self):
        obj = mixer.blend(Feedback)
        assert obj.pk == 1, 'Should save an Feedback instance'

    # To check whether Feedback instance returns proper email string
    def test_str(self):
        obj = mixer.blend(Feedback, email = "test@gmail.com")
        assert str(obj) == "test@gmail.com", 'Feedback instance __str__() should return email'


class TestCategory:
    # To check whether Category instance can be created and saved
    def test_init(self):
        obj = mixer.blend(Category)
        assert obj.pk == 1, 'Should save an Category instance'

    # To check whether Category instance returns proper email string
    def test_str(self):
        obj = mixer.blend(Category, title = "Category Title")
        assert str(obj) == "Category Title", 'Category instance __str__() should return title'
