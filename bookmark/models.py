from django.contrib.auth import get_user_model
from django.db import models

class Bookmark(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookmarks')
    bookmarked_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookmark_of')

    class Meta:
        unique_together = ('user', 'bookmarked_user')
