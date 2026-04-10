from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChildrenSerializer, LoginSerializer, ParentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class ParentCreateView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ParentSerializer(data=request.data)
    

        if serializer.is_valid():
            parent = serializer.save()
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChildrenRegisterView(APIView):
    def post(self, request):
        serializer = ChildrenSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "O‘quvchi muvaffaqiyatli ro‘yxatdan o‘tdi"
            }, status=201)

        return Response(serializer.errors, status=400)
    
class ChildrenLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "success": True,
                "message": "Muvaffaqiyatli logout qilindi"
            })

        except Exception as e:
            return Response({
                "error": "Token noto'g'ri yoki eskirgan"
            }, status=status.HTTP_400_BAD_REQUEST)