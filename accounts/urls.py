from django.urls import path;
from django.contrib.auth import views as auth_views;
from . import views;

urlpatterns = [
    # Empty string = base page
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.home, name="home"),
    path('user/', views.user_page, name="user_page"),
    path('account/', views.account_settings, name="account"),
    path('products/', views.products, name="products"),
    # The name you put in <> must be the same at the view
    path('customer/<str:pk>', views.customer, name="customer"),
    path('create_order/<str:pk>', views.create_order, name="create_order"),
    path('update_order/<str:pk>', views.update_order, name="update_order"),
    path('delete_order/<str:pk>', views.delete_order, name="delete_order"),
    # For resetting the info we are using already done django templates (but can be customized)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    # The names must be given as django relies on those
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    # Luckily django already secures this uid
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete")
]
