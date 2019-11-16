from django.urls import path

from user import views

# `app_name` is used to identify which app we create the URLs from when we
# use the `reverse` function
app_name = 'user'

urlpatterns = [
    # api/user/create/ ... see `app.urls`
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token')
]
