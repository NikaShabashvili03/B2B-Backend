from rest_framework import serializers
from ..models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer 
        fields = ['id', 'firstname', 'lastname', 'email']

class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            customer = Customer.objects.get(email=data['email'])
            if customer.check_password(data['password']):
                return customer
            else:
                raise serializers.ValidationError("Invalid credentials")
        except Customer.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        