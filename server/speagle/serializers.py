from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('dob', 'country', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    # profile here is a Writable Nested Serializer which is
    # a serializer that uses another serializer for a particular field.
    # Recalls this field when defining the UserProfile model,
    # the related_name parameter was set in the OneToOne relationship definition.
    # This is what enabled the use of the profile field in the UserSerializer class.

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
        # password field is set as a write_only field.
        # Meaning that it will be used for deserialization(creating the model)
        # but not for serialization.

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        # By using set_password method, the password is hashed
        # and stored as a hash rather than plaintext.
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.dob = profile_data.get('dob', profile.dob)
        profile.country = profile_data.get('country', profile.country)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance