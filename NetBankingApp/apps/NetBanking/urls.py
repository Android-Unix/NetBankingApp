from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
    path('users/create-user/', views.CreateUserViewSet.as_view({'post': 'post'})),
    path('users/<uuid:pk>/', views.UserViewSet.as_view({'get': 'retrieve_user'})),
    path('users/<uuid:pk>/delete/', views.UserViewSet.as_view({'get': 'delete_user'})),
    path('users/<uuid:pk>/accounts/', views.AccountViewSet.as_view({'get': 'list_accounts'})),
    path('users/<uuid:pk>/accounts/<uuid:account_id>/', views.AccountViewSet.as_view({'get': 'account_details'})),
    path('users/<uuid:pk>/accounts/<uuid:account_id>/delete/', views.AccountViewSet.as_view({'get': 'delete_account'})),
    path('users/<uuid:pk>/accounts/<uuid:senders_account_id>/transfer/', views.TransationsViewSet.as_view({'post': 'transferMoney'})),
    path('users/<uuid:pk>/accounts/<uuid:account_id>/action/', views.AccountViewSet.as_view({'post': 'bankAction'})),
    path('users/<uuid:pk>/accounts/<uuid:account_id>/account-activity/', views.TransationsViewSet.as_view({'get': 'account_activity'})),
    path('users/<uuid:pk>/create-account/', views.AccountViewSet.as_view({'post': 'create_account'})),
    path('transactions/', views.TransationsViewSet.as_view({'get': 'list_transactions'})),

]
