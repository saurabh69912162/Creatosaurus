from rest_framework import serializers
from .models import MyUser


class business_profile_dataSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('__all__')
