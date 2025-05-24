from rest_framework import serializers
from ..models import Category, Attribute


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data
