from django.urls import path
from users import views

urlpatterns = [
    # path('kakao/login/', views.kakao_login, name='kakao_login'),
    # path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    # path('kakao/login/finish/', views.KakaoLogin.as_view(),
    #      name='kakao_login_todjango'),

    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(),
         name='kakao_login_todjango'),
    
    # path('kakao/callback/', views.KakaoLoginView.as_view(), name='kakao_callback'),

    path('github/login/', views.github_login, name='github_login'),
    path('github/callback/', views.github_callback, name='github_callback'),
    path('github/login/finish/', views.GithubLogin.as_view()),

    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view()),

]
