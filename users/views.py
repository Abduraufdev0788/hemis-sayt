from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChildrenSerializer, ParentSerializer

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