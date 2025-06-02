from rest_framework import serializers
from .models import Project, Accountability
from communes.serializers import CommuneSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'prenom', 'telephone', 'role']


class ProjectListSerializer(serializers.ModelSerializer):
    commune = CommuneSerializer(read_only=True)
    created_by = UserBasicSerializer(read_only=True)
    accountability_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'status',
            'commune',
            'start_date',
            'end_date',
            'budget',
            'avancement',           # ← champ avancement ajouté
            'image',
            'created_at',
            'created_by',
            'accountability_count'
        ]

    def get_accountability_count(self, obj):
        return obj.accountability_requests.count()


class ProjectDetailSerializer(ProjectListSerializer):
    class Meta(ProjectListSerializer.Meta):
        fields = ProjectListSerializer.Meta.fields + ['updated_at']


class AccountabilitySerializer(serializers.ModelSerializer):
    citizen = UserBasicSerializer(read_only=True)
    responded_by = UserBasicSerializer(read_only=True)
    project = ProjectListSerializer(read_only=True)

    class Meta:
        model = Accountability
        fields = [
            'id',
            'project',
            'citizen',
            'question',
            'response',
            'status',
            'created_at',
            'updated_at',
            'responded_by',
            'responded_at'
        ]
        read_only_fields = ['status', 'responded_by', 'responded_at']


class AccountabilityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountability
        fields = ['project', 'question']

    def create(self, validated_data):
        validated_data['citizen'] = self.context['request'].user
        return super().create(validated_data)


class AccountabilityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountability
        fields = ['response']

    def update(self, instance, validated_data):
        validated_data['responded_by'] = self.context['request'].user
        return super().update(instance, validated_data)
