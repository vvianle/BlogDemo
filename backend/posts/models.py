from django.db import models
from accounts.models import MyUser
from datetime import datetime

# Create your models here.

# model of a blog
class BlogPost(models.Model):
	author = models.ForeignKey(MyUser)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	title = models.CharField(max_length=50, blank=False)
	content = models.CharField(max_length=1000, blank=False)

	def __str__(self):
		return self.title + ' - ' + self.author.username

# model of a comment
class PostComment(models.Model):
	author = models.ForeignKey(MyUser)
	post = models.ForeignKey(BlogPost)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)
	content = models.CharField(max_length=500, blank=False)

	def __str__(self):
		return self.post.title + ' - ' + self.author.username