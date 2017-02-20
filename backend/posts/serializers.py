from rest_framework import serializers
from .models import *
from accounts.serializers import AuthenticatedUserSerializer

class PostSerializer(serializers.ModelSerializer):
	author = AuthenticatedUserSerializer(read_only=True)
	class Meta:
		model = BlogPost

class CommentSerializer(serializers.ModelSerializer):
	author = AuthenticatedUserSerializer(read_only=True)
	post = PostSerializer(read_only=True)
	class Meta:
		model = PostComment