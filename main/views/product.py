import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Product, Category, Supplier
from ..serializers.product import ProductSerializer
from rest_framework import status
from django.db.models import Q


class ProductsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, categoryId):
        category = Category.objects.filter(id=categoryId).distinct().first()

        if not category:
            return Response({"detail": "Category doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        
        products = Product.objects.filter(category=category).distinct()


        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        supplier_id = request.query_params.get('supplier_id')

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if ordering:
            products = products.order_by(ordering)
        if supplier_id:
            products = products.filter(supplier__id=supplier_id)

        attribute_filters = {
            key.replace("attribute_", "").lower(): value.lower()
            for key, value in request.query_params.items()
            if key.startswith("attribute_")
        }

        if attribute_filters:
            filtered_products = []
            for product in products:
                try:
                    attrs = json.loads(product.attributes)
                    attrs = {k.lower(): str(v).lower() for k, v in attrs.items()}
                except json.JSONDecodeError:
                    continue

                if all(attrs.get(k) == v for k, v in attribute_filters.items()):
                    filtered_products.append(product)

            products = filtered_products
        else:
            products = list(products)

        return Response(ProductSerializer(products, many=True).data)
    

class ProductSingleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        product = Product.objects.filter(id=id).distinct().first()

        if not product:
            return Response({"detail": "Product doesnot exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response(ProductSerializer(product).data)