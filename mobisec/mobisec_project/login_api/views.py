from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from app.models import Users
from django.contrib.auth.hashers import	check_password
from rest_framework_simplejwt.tokens import AccessToken
import jwt

# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = Users.objects.get(email=data.get('email'))
            refresh = RefreshToken.for_user(user)
            response_data = {
		    	'refresh_token': str(refresh),
		    	'access_token': str(refresh.access_token),
		    	'id':str(user.id)
	    	}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
	        return Response({'title':'Error', 'message':f'Registratin is failed because of the error :- {serializer.errors}'})

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email').strip() if request.data.get('email') else None
        password = str(request.data.get('password')).strip()  if request.data.get('password') else None
        # print(email,password)
        if not email or not password:
            return Response({'title':'Error', 'message':'email and password both are mandatory'},status=400)
        user = Users.objects.get(email=email)
        if not user:
            return Response({'title':'Error', 'message':f'No user found'}, status=401)
        correct_pass = check_password(password, user.password)
        if not correct_pass:
            return Response({'title':'Error', 'message':'Incorrect Password'}, status=401)
        if (user):
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            response_data = {
                'refresh_token':str(refresh_token),
                'access_token':str(access_token),
                'id':str(user.id),
                'title':'Success',
                'message':'User loggedin Successfully',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'title':'Error', 'message':'Invalid Username or Password'}, status=400)
        

class FetchUser(APIView):
    def get(self, request):
        jwt_token = request.headers.get('X-Authorization')
        try:
            access_token = AccessToken(jwt_token)
            id = access_token.payload['user_id']
            # print(id)
            user = Users.objects.get(id=id)
            user_data = UserSerializer(user)
            return Response({'title':'Success', 'data':user_data.data}, status=200)
        except Exception as e:
            print('Exception:',e)
            return Response({'title':'Error', 'message':f'Token is either invalid or expired => {e}'}, status=401)