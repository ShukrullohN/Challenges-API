from datetime import timedelta
from django.shortcuts import render
from challenges.serializers import *
from users.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters
from challenges.models import ChallengeModel, MemberModel
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


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
    

class ChallengeMembersView(generics.ListAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        challenge_id = self.kwargs['pk']
        challenge = get_object_or_404(ChallengeModel, id=challenge_id)
        return challenge.members.all()



class SearchChallengeBySecretKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SecretKeySerializer(data=request.data)
        if serializer.is_valid():
            secret_key = serializer.validated_data['secret_key']
            try:
                challenge = ChallengeModel.objects.get(secret_key=secret_key, status=False)  # Ensure it's a private challenge
                return Response({"challenge_id": challenge.id, "message": "Secret key is valid. Please provide the secret password."})
            except ChallengeModel.DoesNotExist:
                return Response({"error": "Invalid secret key or the challenge is not private."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinChallengeWithSecretPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            challenge = ChallengeModel.objects.get(id=pk, status=False)  # Ensure it's a private challenge
        except ChallengeModel.DoesNotExist:
            return Response({"error": "Challenge not found or it is not private."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SecretPasswordSerializer(data=request.data)
        if serializer.is_valid():
            secret_password = serializer.validated_data['secret_password']
            if challenge.secret_password == secret_password:
                # Add user to challenge
                MemberModel.objects.get_or_create(user=request.user, challenge=challenge)
                return Response({"message": "Successfully joined the challenge."})
            else:
                return Response({"error": "Incorrect secret password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DisjoinChallengeView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        challenge_id = kwargs.get('pk')
        user = request.user
        
        try:
            member = Member.objects.get(challenge_id=challenge_id, user=user)
            member.delete()
            return Response({"message": "Successfully disjoined from the challenge."}, status=status.HTTP_204_NO_CONTENT)
        except Member.DoesNotExist:
            return Response({"error": "You are not a member of this challenge."}, status=status.HTTP_404_NOT_FOUND)



class MemberDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer
    queryset = MemberModel.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            challenge_id = kwargs['pk']
            member_id = kwargs['member_id']
            member = MemberModel.objects.get(id=member_id, challenge_id=challenge_id)

            if member.user != request.user and not request.user.is_superuser:
                return Response({"error": "You do not have permission to delete this member."}, status=status.HTTP_403_FORBIDDEN)
            
            member.delete()
            return Response({"message": "Member successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except MemberModel.DoesNotExist:
            return Response({"error": "Member not found in the specified challenge."}, status=status.HTTP_404_NOT_FOUND)



class OwnChallengesView(generics.ListAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChallengeModel.objects.filter(owner=self.request.user)

class ChallengeListView(generics.ListAPIView):
    queryset = ChallengeModel.objects.filter(status=True)
    serializer_class = ChallengeListSerializer
    queryset = ChallengeModel.objects.filter(status=True)  # Only public challenges
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'secret_key']

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
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        challenge = ChallengeModel.objects.filter(pk=pk, owner=self.request.user)
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



class FillTaskView(generics.GenericAPIView):
    serializer_class = FillTaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        challenge_id = self.kwargs['pk']
        challenge = ChallengeModel.objects.get(id=challenge_id)

        # Check if the user is the owner of the challenge
        if challenge.owner != request.user:
            return Response({"detail": "You do not have permission to fill tasks for this challenge."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'view': self})
        serializer.is_valid(raise_exception=True)

        tasks = serializer.validated_data['tasks']

        # Calculate and create tasks for every `limited_time` interval
        current_date = challenge.start_at
        while current_date <= challenge.end_at:
            due_date = current_date
            TasksModel.objects.update_or_create(
                challenge=challenge,
                due_date=due_date,
                defaults={'tasks': tasks}
            )
            current_date += timedelta(days=challenge.limited_time)

        return Response({"detail": "Tasks have been filled successfully."}, status=status.HTTP_200_OK)



class TaskUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UpdateTaskSerializer
    http_method_names = ['put', 'patch']

    def get_object(self): 
        pk = self.kwargs.get('pk')
        return TasksModel.objects.filter(pk=pk).first()

    def update(self, request, *args, **kwargs):
        super(TaskUpdateAPIView, self).update(request, *args, **kwargs)
        response = {
            "success": True,
            "message": "Challenge updated successfully",
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        super(TaskUpdateAPIView, self).partial_update(request, *args, **kwargs)
        response = {
            "success": True,
            "message": "Challenge updated successfully"
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)