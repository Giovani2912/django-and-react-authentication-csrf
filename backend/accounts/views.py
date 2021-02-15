from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from user_profile.models import UserProfile
from .serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator



# MÉTODO QUE PROTEGE O FORMULÁRIO COM O CSRF
@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):

        try:
            isAuthenticated = User.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})




@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    # FUNÇÃO PARA REGISTRAR O USUÁRIO
    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            try:
                if User.objects.filter(username=username).exists():
                    return Response({ 'error': 'Username already exists' })
                else:
                    if len(password) < 6:
                        return Response({ 'error': 'Password must be at least 8 characters' })
                    else:
                        user = User.objects.create_user(username=username, password=password)

                        user.save()

                        user = User.objects.get(id=user.id)

                        user_profile = UserProfile(user=user, first_name='', last_name='', phone='', city='')

                        user_profile.save()

                        return Response({ 'success': 'User created successfully' })
            except:
                return Response({ 'error': 'Something went wrong when registering your account' })
        else:
            return Response({ 'error': 'Password do not match. :(' })





# CLASSE DE LOGIN
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    # FUNÇÃO PARA LOGAR O USUÁRIO
    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            # ACESSANDO A BASE DE DADOS PARA BUSCAR O USUÁRIO E A SENHA
            user = auth.authenticate(username=username, password=password) 
            if user is not None:
                auth.login(request, user)
                return Response({ 'success': 'User authenticated', 'username': username })
            else:
                return Response({ 'error': 'Error Authenticating' })
        except:
            return Response({ 'error': 'Something went wrong when logging in' })






# LOGOUT DA CONTA
class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Logout Successfully' })
        except:
            return Response({ 'error': 'Something went wrong when you logging out' })




# GERAR UM CSRF TOKEN
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )


    def get(self, request, format=None):
        return Response({'success': 'CSRF Cokkie set'})



# DELETAR UM CONTA
class DeleteAccountView(APIView):
    def post(self, request, format=None):
        user = self.request.user

        try:
            user = User.objects.filter(id=user.id).delete()
            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })


class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True)
        return Response(users.data)

        
