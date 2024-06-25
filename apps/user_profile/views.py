from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics, permissions, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from django.db import IntegrityError


# from masters.models import MasterModel
# from products.models import HouseModel
# from store.models import StoreModel
from .models import User, Map

# from products.serializers import HomeSerializer
# from masters.serializers import MasterSerializer
# from store.serializers import StoreModelSerializer
from .playmobile import SendSmsWithPlayMobile, SUCCESS

from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer, UserALLSerializer, \
    UpdateUserSerializer, MapSerializer, ResendPasswordSerializer, ConfirmationSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(GenericViewSet):
    ''' Регистрация юзера '''
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    # @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
    def create(self, request: Request):
        self.serializer_class = RegistrationSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        password = serializer.validated_data['password']

        try:
            user = User.objects.create(phone_number=phone_number, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
        except IntegrityError:
            return Response({'error': 'User with this phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = User.objects.get_or_create(phone_number=phone_number)
        return Response({'token': token.tokens()})

    #
    # @action(['DELETE'], detail=False, permission_classes=[IsAuthenticated])
    # def logout(self, request: Request):
    #     Token.objects.get(user=request.user).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class LoginView(TokenObtainPairView):
# permission_classes = (AllowAny,)
# serializer_class = MyTokenObtainPairSerializer
# from django.contrib.auth import login, authenticate
#
#
# class LoginView(APIView):
#     def post(self, request):
#         phone_number = request.data['phone_number']
#         password = request.data['password']
#         user = authenticate(phone=phone_number, password=password)
#         if not user:
#             login(request, user)

# class LoginView(viewsets.ViewSet):
#     """ Elektron pochta va parolni tekshiradi va autentifikatsiya belgisini qaytaradi."""
#
#     serializer_class = AuthTokenSerializer
#
#     def create(self, request):
#         """Tokenni tasdiqlash va yaratish uchun ObtainAuthToken APIView-dan foydalaning."""
#
#         return ObtainAuthToken().as_view()(request=request._request)
class LoginView(GenericViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
    def login(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            token, created = User.objects.get_or_create(phone_number=phone_number)
            return Response({'token': token.tokens()})
        else:
            return Response({'error': "Invalid phone number or password!"})

    @action(['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        token = request.auth
        if token is not None:
            token.delete()
            return Response({"status": "Successful"})
        else:
            return Response({"status": "No token found"})


class UserProfile(APIView):
    get_serializer_class = None

    def get_object(self, user, pk=None):
        pass

    def get(self, request, **kwargs):
        pass
        # return Response(data, status=200)


class UserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = User.objects.get(id=pk)
        serializer = UserSerializer(users, context={'request': request})
        return Response(serializer.data)


# class UserProductsList(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, pk):
#         users = CustomUser.objects.get(id=pk)
#         serializer = UserProductsSerializer(users, context={'request': request})
#         return Response(serializer.data)


class ResendPasswordView(CreateAPIView):
    serializer_class = ResendPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)

        code = User.mycode2()
        send_sms_result = SendSmsWithPlayMobile("Gipermart.uz\nКод сброса пароля: {}".format(code), phone_number)
        result = send_sms_result.send()  # Sending the SMS

        if result['status'] == SUCCESS:  # Checking the status directly from the result
            user.mycode = code
            user.save()
            return Response({'message': 'SMS успешно отправлено. Проверьте свой телефон для получения кода сброса пароля.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Не удалось отправить SMS. Пожалуйста, попробуйте еще раз позже.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConfirmationView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Аутентификация пользователя
        authenticated_user = authenticate(phone_number=user.phone_number, password=request.data.get('password'))
        if authenticated_user is not None:
            login(request, authenticated_user)

        return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer


class UserProfileList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = User.objects.filter(id=pk)
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return Response(serializer.data)


class MapView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
              mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = (IsAuthenticated,)
