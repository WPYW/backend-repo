from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from wpyw.settings import SECRET_KEY

import requests
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from .models import Users


# Create your views here.
class RegisterAPIView(APIView):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthAPIView(APIView):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(Users, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(Users, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
    	# 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response




BASE_URL = 'http://localhost:8000/api/v1/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'
# KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'
KAKAO_CALLBACK_URI = 'http://localhost:5173'
GITHUB_CALLBACK_URI = BASE_URL + 'accounts/github/callback/'

state = getattr(settings, 'STATE')


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    print(scope)
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&client_secret={client_secret}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    id_token = token_req_json.get('id_token')
    """
    Email Request
    """
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = Users.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': f'no matching social type. please login with {social_user.provider}'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': id_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except Users.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': id_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

# class KakaoLoginView(APIView): #카카오 로그인

#     def get(self, request):
#         rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
#         secret_api_key = getattr(settings, 'SOCIAL_AUTH_KAKAO_SECRET')
#         code = request.GET.get("code")
        
#         print("==========access_token=========")
#         print(code)
#         print("===================")
        
#         redirect_uri = KAKAO_CALLBACK_URI
#         """
#         Access Token Request
#         """
#         print("=================Access Token Request==================")
#         token_req = requests.get(
#             f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&client_secret={secret_api_key}&redirect_uri={redirect_uri}&code={code}")
#         token_req_json = token_req.json()
#         print(token_req_json)
#         error = token_req_json.get("error")
#         if error is not None:
#             raise JSONDecodeError(error)
#         access_token = token_req_json.get("access_token")
#         """
#         Email Request
#         """
#         profile_request = requests.get(
#             "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
#         profile_json = profile_request.json()
#         print("==========profile_json=========")
#         print(profile_json)
#         print("===================")
#         error = profile_json.get("error")
#         if error is not None:
#             raise JSONDecodeError(error)
#         kakao_account = profile_json.get('kakao_account')
#         print("==========kakao_account=========")
#         print(kakao_account)
#         print("===================")
#         """
#         kakao_account에서 이메일 외에
#         카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
#         print(kakao_account) 참고
#         """
#         email = kakao_account.get('email')
#         """
#         Signup or Signin Request
#         """
        
#         try:
#             user = Users.objects.get(email=email)
#             # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
#             # 다른 SNS로 가입된 유저
#             social_user = SocialAccount.objects.get(user=user)
#             print("=======================")
#             print(social_user)
#             print("=======================")
#             if social_user is None:
#                 return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#             if social_user.provider != 'kakao':
#                 return JsonResponse({'err_msg': f'no matching social type. please login with {social_user.provider}'}, status=status.HTTP_400_BAD_REQUEST)
#             # 기존에 kakao로 가입된 유저
#             # encoded_jwt        = jwt.encode({'id': user.email}, wef_key, algorithm='HS256') # jwt토큰 발행
            
#             # serializer = UserSerializer(user)
            
#             serializer = UserSerializer(data=user)
#             if serializer.is_valid():
#                 user = serializer.save()
                
#                 # jwt 토큰 접근
#                 token = TokenObtainPairSerializer.get_token(user)
#                 refresh_token = str(token)
#                 access_token = str(token.access_token)
#                 res = Response(
#                     {
#                         "user": serializer.data,
#                         "message": "register successs",
#                         "token": {
#                             "access": access_token,
#                             "refresh": refresh_token,
#                         },
#                     },
#                     status=status.HTTP_200_OK,
#                 )
                
#                 # jwt 토큰 => 쿠키에 저장
#                 res.set_cookie("access", access_token, httponly=True)
#                 res.set_cookie("refresh", refresh_token, httponly=True)
                
#                 return res
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Users.DoesNotExist:
#             # 기존에 가입된 유저가 없으면 새로 가입
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     # "user": serializer.data,
#                     "message": "login successs",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
            
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
            
#             return res


def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    secret_api_key = getattr(settings, 'SOCIAL_AUTH_KAKAO_SECRET')
    code = request.GET.get("code")
    
    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&client_secret={secret_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    kakao_account = profile_json.get('kakao_account')

    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    email = kakao_account.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = Users.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': f'no matching social type. please login with {social_user.provider}'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 kakao로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        
        if user is not None:
            # serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = JsonResponse(
                {
                    # "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        
        # print(accept_json)
        # return JsonResponse(accept_json)
    except Users.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        
        user = Users.objects.get(email=email)
        
        if user is not None:
            # serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = JsonResponse(
                {
                    # "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        
        # return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
    
    

# def kakao_login(request):
#     rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
#     secret_api_key = getattr(settings, 'SOCIAL_AUTH_KAKAO_SECRET')
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
#     )


# def kakao_callback(request):
#     rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
#     secret_api_key = getattr(settings, 'SOCIAL_AUTH_KAKAO_SECRET')
#     code = request.GET.get("code")
#     redirect_uri = KAKAO_CALLBACK_URI
#     """
#     Access Token Request
#     """
#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&client_secret={secret_api_key}&redirect_uri={redirect_uri}&code={code}")
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     access_token = token_req_json.get("access_token")
#     """
#     Email Request
#     """
#     profile_request = requests.get(
#         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
#     profile_json = profile_request.json()
#     error = profile_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     kakao_account = profile_json.get('kakao_account')
#     """
#     kakao_account에서 이메일 외에
#     카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
#     print(kakao_account) 참고
#     """
#     email = kakao_account.get('email')
#     """
#     Signup or Signin Request
#     """
#     try:
#         user = Users.objects.get(email=email)
#         # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
#         # 다른 SNS로 가입된 유저
#         social_user = SocialAccount.objects.get(user=user)
#         print("=======================")
#         print(social_user)
#         print("=======================")
#         if social_user is None:
#             return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#         if social_user.provider != 'kakao':
#             return JsonResponse({'err_msg': f'no matching social type. please login with {social_user.provider}'}, status=status.HTTP_400_BAD_REQUEST)
#         # 기존에 Google로 가입된 유저
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
#     except Users.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
#         # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)


# class KakaoLogin(SocialLoginView):
#     parser_classes = (MultiPartParser,FormParser,JSONParser)
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = KAKAO_CALLBACK_URI


def github_login(request):
    client_id = getattr(settings, 'SOCIAL_AUTH_GITHUB_CLIENT_ID')
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={GITHUB_CALLBACK_URI}"
    )


def github_callback(request):
    client_id = getattr(settings, 'SOCIAL_AUTH_GITHUB_CLIENT_ID')
    client_secret = getattr(settings, 'SOCIAL_AUTH_GITHUB_SECRET')
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&accept=&json&redirect_uri={GITHUB_CALLBACK_URI}&response_type=code", headers={'Accept': 'application/json'})
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    user_req = requests.get(f"https://api.github.com/user",
                            headers={"Authorization": f"Bearer {access_token}"})
    user_email_req = requests.get(f"https://api.github.com/user/emails",
                            headers={"Authorization": f"Bearer {access_token}"})
    # https://api.github.com/user/emails
    # https://api.github.com/user
    user_json = user_req.json()
    error = user_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    
    user_email_req = user_req.json()
    error = user_email_req.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    email = user_email_req.get("email")
    
    if email == None:
        return JsonResponse({'err_msg': 'failed to get email. please check your github email setting.'}, status=400)
    
    """
    Signup or Signin Request
    """
    try:
        user = Users.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 github가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'github':
            return JsonResponse({'err_msg': f'no matching social type. please login with {social_user.provider}'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 github로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except Users.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)


class GithubLogin(SocialLoginView):
    """
    If it's not working
    You need to customize GitHubOAuth2Adapter
    use header instead of params
    -------------------
    def complete_login(self, request, app, token, **kwargs):
        params = {'access_token': token.token}

    TO

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
    -------------------
    """
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client
