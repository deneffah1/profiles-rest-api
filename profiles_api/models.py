from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """
    Manager class for handling user creation and superuser creation.
    Provides helper methods to create regular users and superusers using email instead of username.
    """
    def create_user(self, email, name, password=None):
        """
        Creates and saves a regular user with the given email, name, and password.

        Args:
            email (str): Email address of the user (must be provided).
            name (str): Full name of the user.
            password (str, optional): Password for the user. Defaults to None.

        Returns:
            UserProfile: The created user object.

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a new superuser with the given email, name, and password.

        Args:
            email (str): Email address of the superuser.
            name (str): Full name of the superuser.
            password (str): Password for the superuser.

        Returns:
            UserProfile: The created superuser object.
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
    
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the system that supports email instead of username for authentication.

    Inherits from:
        AbstractBaseUser: Provides core authentication functionality.
        PermissionsMixin: Adds permission-related fields like is_superuser.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email
    

