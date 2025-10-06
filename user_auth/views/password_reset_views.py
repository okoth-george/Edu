
from user_auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.permissions import AllowAny , IsAuthenticated
from ..serializers.serializers import ResetPasswordSerializer, ResetPasswordConfirmSerializer

class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():          
            email = serializer.validated_data['email']
            try:
              user = User.objects.get(email=email)
            except User.DoesNotExist:
              return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)   
        
            token=str(random.randint(100000,999999))

            cache.set(f"reset_token_{email}", token, timeout=300)  # 10 min expiry

         #  TODO: Send this token via email (SendGrid, SMTP, etc.)
            print(f"Password reset token for {email}: {token}")

            return Response({"message": "Password reset token sent to email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
        

            try:
              user = User.objects.get(email=email)
            except User.DoesNotExist:
              return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

            saved_token = cache.get(f"reset_token_{email}")
            if saved_token != token:
              return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        # update pasword for the user
            user.password = make_password(new_password)
            user.save()

            cache.delete(f"reset_token_{email}")

            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"error": "Old password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password has been changed successfully"}, status=status.HTTP_200_OK)            