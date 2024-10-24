
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AugmentedTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token_repr = super().get_token(user)
        token_repr['username'] = user.username
        return token_repr
