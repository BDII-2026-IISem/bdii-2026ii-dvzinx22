from rest_framework import serializers


from django.contrib.auth import get_user_model

User = get_user_model()


from apps.common.status import RecordStatus


class ProfileSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "status",
            "is_superuser",
            "roles",
        ]
        read_only_fields = ["id", "username", "status", "is_superuser", "roles"]

    def get_roles(self, obj):
        if hasattr(obj, "role_links"):
            return list(
                obj.role_links.filter(
                    status=RecordStatus.ACTIVE,
                    role__status=RecordStatus.ACTIVE,
                ).values_list("role__name", flat=True)
            )
        return []


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if not attrs.get("username") and not attrs.get("email"):
            raise serializers.ValidationError(
                "Informe username o email junto con password."
            )
        return attrs


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    token_type = serializers.CharField()
    access_expires_in = serializers.IntegerField()

from django.contrib.auth import password_validation
from apps.security.models import Role, RoleUser, Resource, ResourceRole


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "status",
            "password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class RoleUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = RoleUser
        fields = [
            "id",
            "user",
            "role",
            "username",
            "role_name",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "username", "role_name"]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class ResourceRoleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    resource_route = serializers.CharField(source="resource.route", read_only=True)
    resource_method = serializers.CharField(source="resource.method", read_only=True)
    resource_name = serializers.CharField(source="resource.name", read_only=True)

    class Meta:
        model = ResourceRole
        fields = [
            "id",
            "role",
            "resource",
            "role_name",
            "resource_route",
            "resource_method",
            "resource_name",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "role_name",
            "resource_route",
            "resource_method",
            "resource_name",
        ]

