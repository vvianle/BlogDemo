from rest_framework import generics, status
from accounts.permissions import *
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from Blog.views import JSONResponse
from django.http import Http404

# Create your views here.
# GET /posts/
class PostListView(generics.ListCreateAPIView):
	serializer_class = PostSerializer
	permission_classes = (AllowAny, )
	authentication_classes = ([])
	queryset = BlogPost.objects.all().order_by('-pk')


# GET /posts/:pk/
class SinglePostView(generics.RetrieveAPIView):
	def get_object(self):
		pk = self.kwargs['pk']
		post = BlogPost.objects.get(pk=pk)
		try:
			return post
		except BlogPost.DoesNotExist:
			raise Http404

	serializer_class = PostSerializer
	permission_classes = (AllowAny, )
	authentication_classes = ([])

class UpdateSinglePostView(generics.UpdateAPIView):
	def get_object(self):
		pk = self.kwargs['pk']
		post = BlogPost.objects.get(pk=pk)
		try:
			return post
		except BlogPost.DoesNotExist:
			raise Http404

	serializer_class = PostSerializer
	permission_classes = (IsAuthorOrIsAdmin, )

# POST /posts/add/
class SubmitPostView(generics.CreateAPIView):
	serializer_class = PostSerializer
	permission_classes = (IsAuthorOrIsAdmin,)
	queryset = BlogPost.objects.all()

	def create(self, request, *args, **kwargs):
		author = request.user
		request_data = request.data
		serializer = PostSerializer(data={'title': self.request.data['title'], "content": self.request.data['content']})
		if serializer.is_valid(raise_exception=True):
			serializer.save(author=author)
			return JSONResponse({'status': 'success'}, status=status.HTTP_200_OK)
		else:
			return JSONResponse({'status': "fail",
								 'data': {"error": "Unable to add post"}},
								status=status.HTTP_400_BAD_REQUEST)


# GET /posts/:id/comments/
class SinglePostCommentsView(generics.ListCreateAPIView):
	serializer_class = CommentSerializer
	permission_classes = (AllowAny, )
	authentication_classes = ([])

	def get_queryset(self):
		pk = self.kwargs['pk']
		post = BlogPost.objects.get(pk=pk)
		queryset = PostComment.objects.filter(post=post)
		return queryset


# POST /posts/:id/comments/add/
class SubmitCommentView(generics.CreateAPIView):
	serializer_class = CommentSerializer
	permission_classes = (IsAuthenticated,)
	queryset = PostComment.objects.all()

	def create(self, request, *args, **kwargs):
		author = request.user
		pk = self.kwargs['pk']
		post = BlogPost.objects.get(pk=pk)
		serializer = CommentSerializer(data={"content": self.request.data['content']})
		if serializer.is_valid(raise_exception=True):
			serializer.save(author=author, post=post)
			return JSONResponse({'status': 'success'}, status=status.HTTP_200_OK)
		else:
			return JSONResponse({'status': "fail",
								 'data': {"error": "Unable to add comment"}},
								status=status.HTTP_400_BAD_REQUEST)



