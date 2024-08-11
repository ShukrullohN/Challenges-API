from django.urls import path
from challenges.views import *

app_name = 'challenges'  

urlpatterns = [
    path('home/', ChallengesHomeView.as_view(), name='home'),
    path('create/', ChallengeCreateAPIView.as_view(), name='create'),
    path('list/', ChallengeListView.as_view(), name='list'),
    path('my-challenges/', MyChallengesView.as_view(), name='my-challenges'),
    path('own-challenges/', OwnChallengesView.as_view(), name='own-challenges'),
    path('search/', ChallengeListView.as_view(), name='challenge-search'),
    path('search-by-secret-key/', SearchChallengeBySecretKeyView.as_view(), name='search-by-secret-key'),
    path('<int:pk>/members/<int:member_id>/delete/', MemberDeleteView.as_view(), name='member delete'),
    path('<int:pk>/members/', ChallengeMembersView.as_view(), name='members'),
    path('<int:pk>/update/', ChallengeUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/detail/', ChallengeDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/delete/', ChallengeDeleteAPIView.as_view(), name='delete'),
    path('<int:pk>/join/', JoinChallengeView.as_view(), name='join-challenge'),
    path('<int:pk>/disjoin/', DisjoinChallengeView.as_view(), name='disjoin-challenge'),
    path('<int:pk>/fill-tasks/', FillTaskView.as_view(), name='fill-tasks'),
    path('<int:pk>/update-tasks/', TaskUpdateAPIView.as_view(), name='update-tasks'),
    path('<int:pk>/join-with-secret-password/', JoinChallengeWithSecretPasswordView.as_view(), name='join-with-secret-password'),
    path('<int:pk>/done/', MarkTaskDoneView.as_view(), name='mark_task_done'),
]