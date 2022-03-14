from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from store.models import Transaction, Product
from django.contrib.auth import get_user_model
from rest_framework import status
from store.api.v1.serializers import ProductSerializer, CreateTransactionSerializer, GetTransactionSerializer

User = get_user_model()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if self.request.user.balance > 0:
            return Product.objects.all()


class GetTransactionViewSet(ModelViewSet):
    serializer_class = GetTransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']


class CreateTransactionViewSet(ModelViewSet):
    serializer_class = CreateTransactionSerializer
    queryset = Transaction.objects.none()
    http_method_names = ['post']
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = request.user
        if serializer.is_valid():
            # We get the product, which user want to buy.
            instance = Product.objects.get(id=serializer.validated_data["product_id"])
            # Here we check user is already owner of the product or not.
            if user.id == instance.owner.id:
                return Response({"response": "You're the owner"})
            # Here we check user's balance is greater or equal to the price of the product
            if user.balance >= instance.price:
                # If above all checks are passed than we create the transaction
                transaction = Transaction(buyer=user,
                                          seller=instance.owner,
                                          price=instance.price,
                                          product=instance)
                transaction.save()
                # Here we detect the price of product from the buyer balance
                user.balance -= instance.price
                user.save()
                # Here we add the amount of product into seller's balance
                seller = User.objects.get(id=instance.owner_id)
                seller.balance += instance.price
                seller.save()
                # Procedure has been completed, now we change the ownership of the product
                instance.owner = user
                instance.save()
                return Response({"response": "You bought product successfully"}, status=status.HTTP_201_CREATED)
            return Response({'response': f"Your current balance is {user.balace}, which is less then actual price of "
                                         f"{instance.name}"})
        return Response({'response': "There is some problem"}, status.HTTP_400_BAD_REQUEST)








