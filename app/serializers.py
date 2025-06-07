from rest_framework import serializers


class MaterialRequestSerializer(serializers.Serializer):
    product_code = serializers.IntegerField()
    quantity = serializers.IntegerField()