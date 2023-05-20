import pytest
from django.contrib.auth import get_user_model


pytestmark = pytest.mark.django_db


class TestUserMode:
    """Test cases for custom User model."""

    def test_create_user_with_email_successful(self):
        """Test that creating user with email as a username is successful."""

        email = 'test@test.com'
        password = 'testpassword123!'
        user = get_user_model().objects.create(
            email=email,
            password=password,
        )

        assert user.email == email
        assert user.check_password(password) is True