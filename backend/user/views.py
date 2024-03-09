from djoser.views import UserViewSet

from .permissions import BlockAnonymousUserMe


class FoodgramUserViewSet(UserViewSet):
    permission_classes = [
        BlockAnonymousUserMe,
    ]
