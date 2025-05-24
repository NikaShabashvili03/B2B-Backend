from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models.category import Category, Attribute
from ..serializers.category import CategorySerializer, AttributeSerializer
from rest_framework import status

class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(parent=None).distinct()

        
        return Response(CategorySerializer(categories, many=True).data)
    

class CategorySingleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        category = Category.objects.filter(id=id).distinct().first()

        if not category:
            return Response({"detail": "Category doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(CategorySerializer(category).data)
    

class CategoryAttributesView(APIView):
    def get(self, request, id):
        category = Category.objects.filter(id=id).distinct().first()

        if not category:
            return Response({"detail": "Category doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        
        attributes = Attribute.objects.filter(category=category).distinct()

        return Response(AttributeSerializer(attributes, many=True).data)