
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from .models import Person
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.decorators import action 


class RegisterAPI(APIView):


    def post(self , request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': True, 
            'message':'user created...'
        }, status.HTTP_201_CREATED)

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        
        if not serializer.is_valid():
             return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        print(user)
        if not user:
            return Response({
            'status': False, 
            'message':'Invalid Credentials...'
        }, status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user = user)
        print(token)
        return Response({'status': True, 'message': 'user login...', 'token' : str(token)}, 
        status.HTTP_201_CREATED)



class PersonAPI(APIView):
    permmission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            print(request.user)
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
      
            paginator = Paginator(objs, page_size)
            serializer = PeopleSerializer(paginator.page(page), many=True)    
            return Response(serializer.data)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'Invalid Page...'
            })
        
       



@api_view(['GET'])
def index(request):
    courses = {
        'c_n' : 'P',
        'l' : ['f' , 'D']
        }
    return Response(courses)



class PeopleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()


    @action(detail=True, methods=['post','GET'])
    def send_mail_to_person(self, request, pk):
        obj = Person.objects.get(pk=pk)
        serializer = PeopleSerializer(obj)
        return Response({
            'status' : True,
            'message' : 'email sent succesfully',
            'data' : serializer.data
        })
    

# Create your views here.
