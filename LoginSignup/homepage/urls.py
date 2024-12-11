from django.urls import include, path
from .views import gallery, viewArtwork, addArtwork, editComment, deleteComment

app_name = 'base'

urlpatterns = [
    path('', gallery, name='gallery'),
    # path('homepage/', views.gallery, name='gallery'),
    path('views/<int:pk>/', viewArtwork, name='view_artwork'),
    path('add/', addArtwork, name='add_artwork'),
    path('edit-comment/<int:pk>/', editComment, name='edit_comment'),
    path('delete-comment/<int:pk>/', deleteComment, name='delete_comment'),
]