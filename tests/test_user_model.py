import pytest
from django.contrib.auth import get_user_model


pytestmark = pytest.mark.django_db


class TestUserMode:
    """Test cases for custom User model."""

    def test_create_user(self):
        '''Test that creating user is successful.'''

        email = 'test@test.com'
        full_name = 'Test User'
        password = 'testpassword123!'
        user = get_user_model().objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
        )

        assert user.email == email
        assert user.full_name == full_name
        assert user.check_password(password) is True
        assert user.is_active is True
        assert user.is_admin is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        '''Test that creating superuser on system is successful.'''

        superuser = get_user_model().objects.create_superuser(
            email='admin@test.com',
            full_name='Admin User',
            password='testpassword123!',
        )

        assert superuser.is_active is True
        assert superuser.is_admin is True
        assert superuser.is_superuser is True

    def test_create_user_with_wrong_data(self):
        '''Test that creating User with bad data raises an error.'''

        with pytest.raises(TypeError):
            get_user_model().objects.create_user()
        with pytest.raises(TypeError):
            get_user_model().objects.create_user(email='')
        with pytest.raises(ValueError):
            get_user_model().objects.create_user(
                email='',
                full_name='Test User',
                password='test'
            )
