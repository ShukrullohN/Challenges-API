from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from users.permissions import IsOwner
from challenges.serializers import *
from challenges.models import ChallengeModel, MemberModel



class MyChallengesView(generics.ListAPIView):
    serializer_class = MyChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChallengeModel.objects.filter(members__user=user)

class JoinChallengeView(generics.GenericAPIView):
    queryset = ChallengeModel.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        challenge = self.get_object()
        user = request.user

        # Check if the user is already a member
        if MemberModel.objects.filter(challenge=challenge, user=user).exists():
            return Response({'status': 'already joined'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the membership
        MemberModel.objects.create(challenge=challenge, user=user)

        return Response({'status': 'joined', 'message': serializer.data}, status=status.HTTP_200_OK)
    


class ChallengeListView(generics.ListAPIView):
    queryset = ChallengeModel.objects.filter(status=True)
    serializer_class = ChallengeListSerializer


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
        serializer = ChallengeDetailSerializers(challenge)
        response = {
            'success': True,
            'data': serializer.data,

        }
        return Response(response, status=status.HTTP_200_OK)



class ChallengeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        challenge = ChallengeModel.objects.filter(pk=pk)
        if not challenge.first():
            response = {
                "status": False,
                "message": "challenge does not found",
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