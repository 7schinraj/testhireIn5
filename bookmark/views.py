from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bookmark
from .serializers import BookmarkSerializer

class BookmarkView(APIView):
    def post(self, request):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bookmark_id):
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
            bookmark.delete()
            return Response({'message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Bookmark.DoesNotExist:
            return Response({'error': 'Bookmark not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    def get(self, request, user_id):
        try:
            # Query the database for bookmarks of the specified user
            bookmarks = Bookmark.objects.filter(user_id=user_id)
            
            # Serialize the bookmarks data
            serializer = BookmarkSerializer(bookmarks, many=True)
            
            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            return Response({'detail': 'Bookmarks not found for the specified user'}, status=status.HTTP_404_NOT_FOUND)