from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Reservation(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserved_by')
    reserved_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()  # The date when the reservation expires


class BlockedCandidate(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_candidates')
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_candidates_by')
    blocked_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()  # The date when the block expires
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 

    
