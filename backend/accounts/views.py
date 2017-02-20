from rest_framework import filters
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from .models import MyUser
from .permissions import *
from .serializers import *
from Blog.views import JSONResponse
from rest_framework.authtoken.models import Token

# POST /login/
class LoginView(GenericAPIView):
  permission_classes = (AllowAny, )
  authentication_classes = ([])
  serializer_class = LoginSerializer

  def post(self, request, format=None):
      self.serializer = self.get_serializer(data=request.data)
      self.serializer.is_valid(raise_exception=True)
      self.user = self.serializer.validated_data['user']
      if self.user:
          token = Token.objects.get(user=self.user)
          return JSONResponse({"token": token.key}, status=status.HTTP_200_OK)


#GET /members/
#POST /members/
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = MyUser.objects.all()


# GET /members/profile/
# PUT /members/profile/
# DELETE /members/profile/
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAdmin,)
    renderer_classes = (JSONRenderer,)

    def get_object(self):
        return MyUser.objects.get(pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        # Update password
        user = self.get_object()
        serializer.save()
        if "password" in self.request.data and self.request.data["password"] != "":
            password_serializer = ChangePasswordUserSerializer(data={"password": self.request.data["password"]})
            if password_serializer.is_valid(raise_exception=True):
                user.set_password(self.request.data["password"])
                user.save()
                
    def perform_destroy(self, instance):
        instance.is_active = 0
        instance.save()


# GET /members/profile/
# PUT /members/profile/
class AuthenticatedUserDetail(generics.RetrieveUpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get_object(self):
        return self.request.user


# POST /members/profile/reset_password/
class UserSetPassword(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = ChangePasswordUserSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        user = request.user
        request_data = request.data
        print (request_data)
        if user.check_password(request_data["current_password"]):
            serializer = ChangePasswordUserSerializer(data={"password": self.request.data["new_password"]})
            if serializer.is_valid(raise_exception=True):
                if "new_password" in request_data:
                    user.set_password(request_data["new_password"])
                    user.save()
                    return JSONResponse({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return JSONResponse({'status': "fail",
                                 'data': {"password": "Current password is not correct"}},
                                status=status.HTTP_400_BAD_REQUEST)
