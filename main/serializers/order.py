from rest_framework import serializers
from ..models import OrderItem, Order, Product


class InvoiceItemSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    line_total = serializers.SerializerMethodField()

    def get_line_total(self, obj):
        return obj['quantity'] * obj['price_per_unit']

class InvoiceSerializer(serializers.Serializer):
    invoice_number = serializers.CharField()
    order_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    shipping_address = serializers.CharField()
    order_date = serializers.DateTimeField()
    items = InvoiceItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)





class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    estimated_delivery_date = serializers.DateField(required=False, allow_null=True)
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        
        for item in value:
            product = item['product']
            quantity = item['quantity']
            if quantity > product.stock_quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for product {product.name}. Requested: {quantity}, Available: {product.stock_quantity}"
                )
        return value

    def create(self, validated_data):
        customer = self.context['request'].user
        shipping_address = validated_data['shipping_address']
        estimated_delivery_date = validated_data.get('estimated_delivery_date', None)
        items_data = validated_data['items']

        total_price = 0
        for item in items_data:
            total_price += item['product'].price * item['quantity']

        order = Order.objects.create(
            customer=customer,
            shipping_address=shipping_address,
            estimated_delivery_date=estimated_delivery_date,
            total_price=total_price
        )

        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_per_unit=product.price
            )
            product.stock_quantity -= quantity
            product.save()

        return order

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_per_unit']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.company_name', read_only=True)
    invoice = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'order_date', 'total_price', 'status', 'payment_status',
                  'tracking_number', 'shipping_address', 'estimated_delivery_date', 'items', 'invoice']

    def get_invoice(self, obj):
        # Generate invoice number (e.g. ORD + zero padded order id)
        invoice_number = f"INV-{obj.id:06d}"
        
        # Build invoice items list
        invoice_items = []
        for item in obj.items.all():
            invoice_items.append({
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price_per_unit': item.price_per_unit,
            })

        invoice_data = {
            'invoice_number': invoice_number,
            'order_id': obj.id,
            'customer_name': obj.customer.company_name,
            'shipping_address': obj.shipping_address,
            'order_date': obj.order_date,
            'items': invoice_items,
            'total_price': obj.total_price,
        }
        serializer = InvoiceSerializer(invoice_data)
        return serializer.data