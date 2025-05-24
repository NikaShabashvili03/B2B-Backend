from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Cart, Order
from ..serializers.order import OrderCreateSerializer, OrderSerializer

class SubmitOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart.items.select_related('product')
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'shipping_address': request.data.get('shipping_address'),
            'estimated_delivery_date': request.data.get('estimated_delivery_date'),
            'items': [
                {'product': item.product.id, 'quantity': item.quantity} for item in cart_items
            ]
        }

        serializer = OrderCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()

            cart_items.delete()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user
        orders = Order.objects.filter(customer=customer).order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)