from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', PostListView.as_view(), name='post_list_view'),
	url(r'^(?P<pk>\d+)/$', SinglePostView.as_view(), name='single_post_view'),
	url(r'^(?P<pk>\d+)/edit/$', UpdateSinglePostView.as_view(), name='update_single_post_view'),
	url(r'^(?P<pk>\d+)/comments/$', SinglePostCommentsView.as_view(), name='single_post_comments_view'),
	url(r'^(?P<pk>\d+)/comments/add/$', SubmitCommentView.as_view(), name='submit_comment_view'),
	url(r'^add/$', SubmitPostView.as_view(), name='submit_post_view'),
]