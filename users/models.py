import os
import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Manager

from core.models import AuditableModel


def user_image_file_path(instance, filename):
    """
        Generate file path for new user image
    """

    ext = filename.split('.')[1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/users_pics/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
            Creates and save a new user
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
            Creates and saves a new superuser
        """

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, AuditableModel, PermissionsMixin):
    """
        Creates user model that supports using email
    """

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    bio = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to=user_image_file_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class FollowManager(Manager):
    def follow(self, follower, followed):
        follow_relationship = self.model()
        follow_relationship.follower = follower
        follow_relationship.followed = followed

        follow_relationship.save()

        return follow_relationship

    def unfollow(self, follower, followed):
        try:
            follow_relationship = self.get(follower=follower, followed=followed)
            follow_relationship.delete()
            return True
        except FollowingUsers.DoesNotExist:
            return False

    def is_following(self, follower, followed):
        return self.filter(follower=follower, followed=followed).exists()


class FollowingUsers(AuditableModel):
    follower = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(User, related_name="followed_users", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "follower",
            "followed",
        )

    objects = FollowManager()
