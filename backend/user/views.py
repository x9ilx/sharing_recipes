from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import OnlyAuth
from recipe.renderers import SubscribeRenderer
from user.serializers import (
    SubscriptionPostSerializer,
    SubscriptionsGetSerializer,
)

from .permissions import BlockAnonymousUserMe

user_model = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    permission_classes = [
        BlockAnonymousUserMe,
    ]

    def delete_subscription(self, current_user, author):
        if current_user.subscribes.filter(author=author).exists():
            current_user.subscribes.filter(author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Подписка не оформлена'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def add_subscription(self, current_user, author, context):
        if current_user == author:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if current_user.subscribes.filter(author=author).exists():
            return Response(
                {'errors': 'Подписка уже оформлена'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {}
        data['user'] = current_user.pk
        data['author'] = author.pk

        serializer = SubscriptionPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        result = SubscriptionsGetSerializer(instance=instance, context=context)
        return Response(result.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['DELETE', 'POST'],
        url_path='subscribe',
        url_name='user-subscribe',
        permission_classes=[OnlyAuth],
        renderer_classes=[SubscribeRenderer],
    )
    def user_subscribe(self, request, id=-1):
        author = get_object_or_404(user_model, pk=id)
        current_user = request.user
        recipes_limit = self.request.GET.get('recipes_limit', -1)

        if request.method == 'POST':
            context = {
                'recipes_limit': recipes_limit,
                'request': request,
            }
            return self.add_subscription(current_user, author, context)

        if request.method == 'DELETE':
            return self.delete_subscription(current_user, author)

    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=[OnlyAuth],
        renderer_classes=[SubscribeRenderer],
    )
    def user_get_subscriptions(self, request):
        current_user = request.user
        recipes_limit = self.request.GET.get('recipes_limit', -1)

        context = {
            'recipes_limit': recipes_limit,
            'request': request,
        }

        subscribes = self.paginate_queryset(current_user.subscribes.all())
        result = SubscriptionsGetSerializer(
            subscribes, many=True, context=context
        )

        return self.get_paginated_response(result.data)
