from django.urls import path
from django.shortcuts import redirect
from . import views
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    TopicsListView,
    TopicDetailView,
    AddCommentView,
    EditProfileView,
    CreateTopicView,
    ChangePasswordView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', TopicsListView.as_view(), name='topics_list'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('topics/create/', CreateTopicView.as_view(), name='create_topic'),

    path('topic/<int:pk>/delete/', views.delete_topic_view, name='delete_topic'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),

    path('', lambda request: redirect('topics_list'), name='root_redirect'),
]
