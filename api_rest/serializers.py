from rest_framework import serializers
from .models import User, Region, Commune, Address, Hotel, Room, Reservation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'name', 'last_name', 'email', 'phone_number', 'rut', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class CommuneSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Commune
        fields = ['id', 'name', 'region']


class AddressSerializer(serializers.ModelSerializer):
    commune = CommuneSerializer()

    class Meta:
        model = Address
        fields = ['id', 'street', 'number', 'city', 'postal_code', 'commune']

class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'category', 'address']


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()

    class Meta:
        model = Room
        fields = ['id', 'type', 'capacity', 'price', 'hotel']

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    room = RoomSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'check_in_date', 'check_out_date', 'number_of_guests', 'user', 'room']