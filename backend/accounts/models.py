from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Customize User
class UserManager(BaseUserManager):
	def _create_user(self, username, email, password):
		"""
		Create and save an User with the given email, date username and password.
		"""
		now = datetime.now()
		if username is None:
			raise ValueError('Must include username')
		if email is None:
			raise ValueError('Must include email')
		email = self.normalize_email(email)
		user = self.model(
			email=self.normalize_email(email),
			username=username,
			date_joined=now
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username=None, email=None, password=None):
		"""Create and save an User with the given email and password.
		"""
		return self._create_user(username, email, password)

	def create_superuser(self, username, email, password):
		"""Create and save a superuser with the given email and password.
		"""
		user = self._create_user(username, email, password)
		user.is_admin = True
		user.is_author = True
		user.save(using=self._db)
		return user


class AbstractUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True)
	username = models.CharField(max_length=100, unique=True)
	fullname = models.CharField(max_length=255, blank=True, default="")
	date_joined = models.DateTimeField(default=datetime.now, blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_author = models.BooleanField(default=False)

	class Meta:
		abstract = True

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username

	def get_full_name(self):
		return self.fullname

	def get_short_name(self):
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		return self.is_admin


class MyUser(AbstractUser):
	"""
	Concrete class of AbstractUser.
	"""
	class Meta(AbstractUser.Meta):
		swappable = 'AUTH_USER_MODEL'


# generate a token for each user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
