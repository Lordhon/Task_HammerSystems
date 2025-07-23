import random
import string

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from User.models import User
import time
from rest_framework import status

from User.serializer import CodeSerializer


def generate_code():
    return str(random.randint(1000 ,9999))

def generate_invite_code():
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=6))
        if not User.objects.filter(invite_code=code).exists():
            return code


class SendCode(APIView):
    def post(self, request):

        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            time.sleep(2)
            code = generate_code()
            phone = serializer.validated_data['phone_number']
            if User.objects.filter(phone_number=phone).exists():
                user = User.objects.get(phone_number=phone)
                user.code = code
                user.save()
                return Response({'code': code, 'message': 'Код для входа'})
            else: user = User.objects.create(phone_number=phone , invite_code=generate_invite_code() , code=code)


            return Response({'code': code , 'message': 'Код для входа'})
        return Response({'message': 'Phone required'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyCode(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('code')
        if not phone or not code:
            return Response({'message': 'Телефон и код обязательные поля'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone_number=phone)
            if user.code !=code  or user.phone_number != phone:
                return Response({'message': 'не правильный код или номер'} , status=status.HTTP_400_BAD_REQUEST)
            if user.code == code:

                refresh = RefreshToken.for_user(user)

                return Response({'refresh': str(refresh),'access': str(refresh.access_token)})
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        referals = User.objects.filter(activated = user)
        return Response({
            'phone_number': user.phone_number,
            'invite_code': user.invite_code,
            'activated': user.activated.invite_code   if user.activated else None,
            'referals': [ref.phone_number for ref in referals]
        })



class ActivateCode(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        code = request.data.get('invite_code')
        if not code:
            return Response({'message': 'Код приглошения обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user

        if user.activated is not None:
            return Response({'message': 'Вы уже вводили код'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            invite_code = User.objects.get(invite_code=code)
        except User.DoesNotExist:
            return Response({'message': 'Инвайт код не был найден'}, status=status.HTTP_404_NOT_FOUND)
        if invite_code == user:
            return Response({'message': 'Нельзя вводить свой код'}, status=400)

        user.activated = invite_code
        user.save()
        return Response({'message': 'Инвайт код успешно активирован'})








