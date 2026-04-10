from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TeacherRegisterSerializer


class TeacherRegisterView(APIView):
    def post(self, request):
        serializer = TeacherRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "O‘qituvchi yaratildi"
            })

        return Response(serializer.errors, status=400)