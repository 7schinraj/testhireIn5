from django.urls import path
from .views import BlockCandidateView, randomEndpoint

urlpatterns = [
    path('blockcandidate/', BlockCandidateView.as_view(), name='block-candidate'),
    path('random/<str:rf_token>', randomEndpoint, name='randomEndpoint')
]
