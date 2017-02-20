from rest_framework.permissions import BasePermission
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAdminOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow admin to edit.
	"""
	def has_permission(self, request, view):
		if request.user.is_authenticated():
		# Read permissions are given to any request
			if request.method in permissions.SAFE_METHODS:
				return True
			# Write permissions are only given to the admin.
			else:
				return request.user.is_admin
		else:
			raise PermissionDenied("You must be logged in to view this.")


class IsAuthenticated(BasePermission):
	def has_permission(self, request, view):
		return request.user.is_authenticated()


class IsAdmin(BasePermission):
	def has_permission(self, request, view):
		if request.user.is_authenticated():
			return request.user.is_admin
		else:
			raise PermissionDenied("You must be logged in to view this.")


class IsAuthorOrIsAdmin(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.user.is_authenticated():
			# permissions are given to author who owns the post or admin
			return (obj.user == request.user and request.user.is_author) or request.user.is_admin
		else:
			raise PermissionDenied("You must be logged in to view this.")

	def has_permission(self, request, view):
		if request.user.is_authenticated():
			# permissions are given to any author or admin
			return (request.user.is_author or request.user.is_admin)
		else:
			raise PermissionDenied("You must be logged in to view this.")

