from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import OnlyAuth

from .permissions import BlockAnonymousUserMe

user_model = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    permission_classes = [
        BlockAnonymousUserMe,
    ]

    @action(
        detail=True,
        methods=['POST'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=[OnlyAuth],
    )
    def user_subscribe(self, request, id=-1):
        author = get_object_or_404(user_model, pk=id)
        current_user = request.user
        print(
            current_user.subscribes.filter(author=author).values_list('author')
        )
        if current_user.subscribes.filter(author=author).exists():
            return Response(
                {'errors': 'Подписка уже оформлена'}, status=status.HTTP_200_OK
            )
        return Response({'sub': False}, status=status.HTTP_400_BAD_REQUEST)
