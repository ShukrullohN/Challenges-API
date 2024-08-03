from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from users.permissions import IsOwner
from challenges.serializers import *
from challenges.models import ChallengeModel


class ChallengeListView(generics.ListAPIView):
    serializer_class = ChallengeListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ChallengeModel.objects.all()

class ChallengeCreateAPIView(generics.CreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class ChallengeUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UpdateChallengeSerializer
    http_method_names = ['put', 'patch']

    def get_object(self): 
        pk = self.kwargs.get('pk')
        return ChallengeModel.objects.filter(pk=pk).first()

    def update(self, request, *args, **kwargs):
        super(ChallengeUpdateAPIView, self).update(request, *args, **kwargs)
        response = {
            "success": True,
            "message": "Challenge updated successfully",
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        super(ChallengeUpdateAPIView, self).partial_update(request, *args, **kwargs)
        response = {
            "success": True,
            "message": "Challenge updated successfully"
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)

class ChallengeDetailAPIView(APIView):
    def get(self, request, pk):
        challenge = generics.get_object_or_404(ChallengeModel, pk=pk)
        serializer = ChallengeSerializer(challenge)
        response = {
            'success': True,
            'book': serializer.data,

        }
        return Response(response, status=status.HTTP_200_OK)

class ChallengeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        challenge = ChallengeModel.objects.filter(pk=pk)
        if not challenge.first():
            response = {
                "status": False,
                "message": "Product does not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(challenge.first(), request)
        challenge.delete()
        response = {
            "status": True,
            "message": "Successfully deleted"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class ChallengeFillTasks(APIView):
    pass