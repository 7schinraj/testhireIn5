from rest_framework import serializers
from .models import BlockedCandidate
from staff.models import StaffUser

class CandidateBlockSerializer(serializers.ModelSerializer):
    candidate_id = serializers.IntegerField()
    blocked_by_id = serializers.PrimaryKeyRelatedField(queryset=StaffUser.objects.all(), source='blocked_by')  # Use PrimaryKeyRelatedField to handle StaffUser ID
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = BlockedCandidate
        fields = ['candidate_id', 'blocked_by_id', 'amount_paid']

    def create(self, validated_data):
        candidate_id = validated_data.pop('candidate_id')
        blocked_by_id = validated_data.pop('blocked_by_id') 
        amount_paid = validated_data.pop('amount_paid')
        candidate = StaffUser.objects.get(pk=candidate_id)
        validated_data['candidate'] = candidate
        validated_data['blocked_by_id'] = blocked_by_id  
        validated_data['amount_paid'] = amount_paid
        print(validated_data)
        return BlockedCandidate.objects.create(**validated_data)
