from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel
from .serializers import UserSignupSerializer, UserLoginSerializer
from .authentication import JWTHandler


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            hashed_password = make_password(data["password"])

            user_id = UserModel.create_user(
                data["first_name"],
                data["last_name"],
                data["email"],
                hashed_password,
                data.get("phone"),
                data.get("dob"),
                data["gender"],
                data.get("address"),
                data["role_type"],
            )

            return Response(
                {"message": "User created successfully", "user_id": user_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        """
        Handles user login.
        Only allows login for approved users.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = UserModel.get_user_by_email(data["email"])

            if user and check_password(data["password"], user["password"]):
                

                # Generate tokens for approved users
                access_token, refresh_token = JWTHandler.generate_tokens(user["id"])
                return Response({
                    "message": "Login successful",
                    "user": {
                        "id": user["id"],
                        "email": user["email"],
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "role_type": user["role_type"]
                    },
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)