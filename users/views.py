import os

from django.contrib.auth.models import send_mail
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import EmailSerializer, TokenSerializer, UserSerializer
from api_yamdb.settings import SIMPLE_JWT


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, **kwargs):
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid()
        self.perform_update(serializer)

        return Response(serializer.data)


def send_confirmation_code(subject, message, recipient):
    send_mail(
        subject=subject,
        message=message,
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[recipient]
    )


class ConfirmCodeView(views.APIView):
    serializer_class = EmailSerializer

    def action(self, user, serializer, token):
        code = token.encode(user.get_payload())
        send_confirmation_code(
            subject='Hi',
            message=f'Your code is: {code}',
            recipient=user.email
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        User.objects.get_or_create(email=request.data.get('email'))
        user = get_object_or_404(User, email=request.data.get('email'))
        token = TokenBackend(
            SIMPLE_JWT['ALGORITHM'],
            signing_key=SIMPLE_JWT['SIGNING_KEY'],
        )

        return self.action(user, serializer, token)


class TokenView(ConfirmCodeView):

    serializer_class = TokenSerializer

    def action(self, user, serializer, token):
        payload = token.decode(self.request.data.get('confirmation_code'))

        if payload == user.get_payload():
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
