from rest_framework import serializers
from .models import Professor, Session, Formula

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    professor_1_name = serializers.CharField(source="professor_1.name", read_only=True)
    professor_2_name = serializers.CharField(source="professor_2.name", read_only=True)

    class Meta:
        model = Session
        fields = ["session_id", "date", "time", "professor_1_name", "professor_2_name"]


class FormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formula
        fields = ["formula"]