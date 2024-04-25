from django.urls import path
from .views import BookmarkView

urlpatterns = [
    path('', BookmarkView.as_view()), # Create Bookmarks
    path('<int:bookmark_id>', BookmarkView.as_view()), # Delete Bookmarks
    path('users/<int:user_id>/', BookmarkView.as_view(), name='user-bookmarks'), # Get Bookmarks By User
]
