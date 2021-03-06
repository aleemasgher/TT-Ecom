from rest_framework import serializers
from store.models import Product, Transaction


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'owner', 'name', 'price', 'file']


class GetTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'buyer', 'seller', 'product', 'price', 'created']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['buyer'] = instance.buyer.username
        data['seller'] = instance.seller.username
        data['product'] = instance.product.name
        return data


class CreateTransactionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

