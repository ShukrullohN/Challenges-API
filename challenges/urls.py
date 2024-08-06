from django.urls import path
from challenges.views import *

app_name = 'challenges'  

urlpatterns = [
    path('create/', ChallengeCreateAPIView.as_view(), name='create'),
    path('list/', ChallengeListView.as_view(), name='list'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
    path('<int:pk>/update/', ChallengeUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/detail/', ChallengeDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/delete/', ChallengeDetailAPIView.as_view(), name='delete'),
    path('<int:pk>/join/', JoinChallengeView.as_view(), name='join-challenge'),

]