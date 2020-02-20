from django.urls import path
from . import views

urlpatterns = [
    path('' , views.homePage , name = 'home'),
    path('users/', views.UserViewSet.as_view({'get' : 'list'})) ,
    path('users/create-user/' , views.CreateUserViewSet.as_view({'post' : 'post'})) ,
    path('users/<uuid:pk>/' , views.UserViewSet.as_view({'get' : 'retrieve_user'})) ,
    path('users/<uuid:pk>/delete/' , views.UserViewSet.as_view({'get' : 'delete_user'})),
    path('users/<uuid:pk>/accounts/' , views.AccountViewSet.as_view({'get' : 'list_accounts'})),
    path('users/<uuid:pk>/accounts/<int:account_no>/' , views.AccountViewSet.as_view({'get' : 'account_details'})),
    path('users/<uuid:pk>/accounts/<int:account_no>/delete/' , views.AccountViewSet.as_view({'get' : 'delete_account'})),
    path('users/<uuid:pk>/accounts/<int:account_no>/transfer/' , views.TransationsViewSet.as_view({'post' : 'transferMoney'})),
    path('users/<uuid:pk>/accounts/<int:account_no>/action/' , views.AccountViewSet.as_view({'post' : 'bankAction'})),
    path('users/<uuid:pk>/create-account/' , views.AccountViewSet.as_view({'post' : 'create_account'})),
    path('transactions/', views.TransationsViewSet.as_view({'get' : 'list_transactions'})) ,

]
