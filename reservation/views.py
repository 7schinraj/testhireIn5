from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .models import BlockedCandidate
from .serializers import CandidateBlockSerializer
from datetime import datetime, timedelta
from staff.models import StaffUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

class BlockCandidateView(APIView):
    def post(self, request):
        serializer = CandidateBlockSerializer(data=request.data)
        if serializer.is_valid():
            # Get validated data after ensuring serializer is valid
            candidate_id = serializer.validated_data.get('candidate_id')
            blocked_by_id = serializer.validated_data.get('blocked_by')
            amount_paid = serializer.validated_data.get('amount_paid')

            print("Validated data: candidate_id={}, blocked_by_id={}, amount_paid={}".format(candidate_id, blocked_by_id, amount_paid))

            # Check if the candidate_id and blocked_by_id are provided
            if candidate_id is None or blocked_by_id is None:
                return Response({'error': 'candidate_id and blocked_by are required fields'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the candidate is already blocked
            candidate = StaffUser.objects.filter(pk=candidate_id).first()
            if candidate is None:
                return Response({'error': 'Candidate not found'}, status=status.HTTP_400_BAD_REQUEST)

            if BlockedCandidate.objects.filter(candidate=candidate).exists():
                return Response({'error': 'Candidate is already blocked'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the StaffUser instance for blocked_by
            
            print(request.data['blocked_by_id'])
            blocked_by = get_object_or_404(StaffUser, pk=request.data['blocked_by_id'])
            print(blocked_by)
            
            
            # Calculate the end date for the block (e.g., 5 days from today)
            end_date = datetime.now() + timedelta(days=5)
            print("Block expiry date:", end_date)
            
            # Create the BlockedCandidate instance with all required fields
            blocked_candidate = BlockedCandidate.objects.create(
                candidate=candidate,
                blocked_by=blocked_by,  # Pass the StaffUser instance
                expiry_date=end_date,
                amount_paid=amount_paid
            )

            # Serialize the created instance and return the response
            serializer = CandidateBlockSerializer(blocked_candidate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If serializer is not valid, return the errors
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(('GET',)) 
@permission_classes([permissions.AllowAny])
def randomEndpoint(request, rf_token):
    if rf_token == 'AB CD EF GH IJ':
        return Response({
            'status': True
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'status': False
        }, status=status.HTTP_400_BAD_REQUEST)
