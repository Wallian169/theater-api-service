from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "name", "description", "genres", "actors")


class PlayListDetailSerializer(PlaySerializer):
    actors = serializers.SlugRelatedField(
        slug_field="full_name",
        read_only=True,
        many=True)
    genres = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
        many=True
    )

    class Meta:
        model = Play
        fields = ("id", "name", "description", "actors", "genres")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    theatre_hall = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    tickets_available = serializers.IntegerField()

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "poster", "tickets_available")


class PerformanceInTicketSerializer(PerformanceListSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformancePosterSerializer(PerformanceSerializer):
    class Meta:
        model = Performance
        fields = ("id", "poster")


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatre_hall,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketListSerializer(TicketSerializer):
    performance = PerformanceInTicketSerializer(many=False, read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
