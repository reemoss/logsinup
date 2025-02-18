from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import DroneUser,ImageWithDetails,Gallery
from django.conf import settings

class DroneUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    citizenship_url = serializers.SerializerMethodField()
    regd_document_url = serializers.SerializerMethodField()

    class Meta:
        model = DroneUser
        fields = [
            'id', 'first_name', 'last_name', 'password', 'password2', 'address',
            'contact_no', 'email', 'drone_experience', 'citizenship_upload',
            'citizenship_url', 'involvement_type', 'organization_name', 'organization_weblink',
            'organization_social_media_link', 'regd_document_upload', 'regd_document_url'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'organization_name': {'required': False},
            'organization_weblink': {'required': False},
            'organization_social_media_link': {'required': False},
            'regd_document_upload': {'required': False},
        }

    def validate_email(self, value):
        if DroneUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, attrs):
        # Validate passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })

        # Validate organizational fields if involvement_type is 'organizational'
        if attrs.get('involvement_type') == 'organizational':
            if not attrs.get('organization_name'):
                raise serializers.ValidationError({
                    "organization_name": "Organization name is required for organizational involvement."
                })
            if not attrs.get('regd_document_upload'):
                raise serializers.ValidationError({
                    "regd_document_upload": "Registration document is required for organizational involvement."
                })

        return attrs

    def create(self, validated_data):
        # Remove password2 from the data as it's only used for validation
        password2 = validated_data.pop('password2', None)
        email = validated_data.get('email')
        
        # Set username to email
        validated_data['username'] = email
        
        # Create the user instance
        user = DroneUser.objects.create_user(
            password=validated_data.pop('password'),
            **validated_data
        )
        
        return user

    def get_citizenship_url(self, obj):
        if obj.citizenship_upload:
            base_url = self.context.get('base_url', '')
            return f"{base_url}{obj.citizenship_upload.url}"
        return None

    def get_regd_document_url(self, obj):
        if obj.regd_document_upload:
            base_url = self.context.get('base_url', '')
            return f"{base_url}{obj.regd_document_upload.url}"
        return None


class DroneUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Get the user by email
            try:
                user = DroneUser.objects.get(email=email)
                # Check if the user can be authenticated with these credentials
                if user.check_password(password):
                    attrs['user'] = user
                    return attrs
            except DroneUser.DoesNotExist:
                pass

            raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

class ImageWithDetailsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageWithDetails
        fields = ['id', 'title', 'description','image','image_url']

    def get_image_url(self, obj):
        if obj.image:
            base_url = self.context.get('base_url', '')
            return f"{base_url}{obj.image.url}"
        return None

class GallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ['id', 'image', 'image_url', 'created_at']

    def get_image_url(self, obj):
        if obj.image:
            base_url = self.context.get('base_url', '')
            return f"{base_url}{obj.image.url}"
        return None


