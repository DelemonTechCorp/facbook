# serializers.py
from rest_framework import serializers
from .models import Properties
from .models import Property, PropertyImage, PropertyCategory, Location, Developer

class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'



class PropertyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategory
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'image')

# class PropertySerializer(serializers.ModelSerializer):
#     images = PropertyImageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Property
#         fields = '__all__'
class PropertySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    location_name = serializers.CharField(source='location.city')
    developer_name = serializers.CharField(source='developer.name', allow_null=True)

    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
