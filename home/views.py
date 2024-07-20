from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from .models import Person #importing model person
from .serializers import PersonSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes # importing package for function based api-view
from rest_framework.response import Response
from rest_framework.views import APIView # importing package for class based api-view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

# SignUp or registration here permission class in null so any one can get it without authentication

class RegisterAPI(APIView):
    permission_classes=[] #used to acess without authentication
    def post(self, request):
        _data = request.data
        serializer = RegisterSerializer(data = _data)
        
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        serializer.save()
        return Response({'message':'User Created'}, status= status.HTTP_201_CREATED)

# SignIn or login here permission class in null so any one can get it without authentication

class LoginAPI(APIView):
    permission_classes=[] #used to acess without authentication
    def post(self, request):
        _data = request.data
        serializer = LoginSerializer(data =_data)
        if not serializer.is_valid():
            return Response({'message':'Invalid Credential'}, status= status.HTTP_404_NOT_FOUND)
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        print(user)
        if not user:
            return Response({"message":"Invalid"},status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message":"Login Sucessfully", "token":str(token)},status= status.HTTP_201_CREATED)

# here permissionis only for the logined person

class ClassPerson(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        try:
            # objperson = person.objects.filter(team__isnull=False)
            objPerson = Person.objects.all()
            page = request.GET.get('page',1)
            page_size = 2
            paginator = Paginator(objPerson,page_size)
            # serializer = PersonSerializer(objPerson,many = True)
            serializer = PersonSerializer(paginator.page(page),many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'message':'Invalide Page Number'
            })
    def post(self,request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

#here no one can access it becuase the permission class is not set  

@api_view(['GET', 'POST', 'PUT'])
def index(request):
    if request.method == 'GET':
        people_detail = {
            'name':'shahil',
            'age':21,
            'job':'developer'
        }
        return Response(people_detail)
    elif request.method == 'POST':
        print("This is a POST method")
        return Response("This is a POST method")
    elif request.method == 'PUT':
        print('This is a PUT method')
        return Response("This is a PUT method")

# here permission class in null so any one can get it without authentication
 
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([])
def person(request):
    if request.method == 'GET':
        objPerson = Person.objects.all()
        serializer = PersonSerializer(objPerson,many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data=data, partial = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message':'Person Deleted'})

#Custom Pagination class 

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page'
    
#permission is allowed to any one with out authenticatioon
            
class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [] # any one can access it
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    pagination_class = CustomPagination
    
    # for searching data by using 
    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset
        
        if search:
            queryset = queryset.filter(name__startswith = search)
            
        #Paginate the queryset
        
        paginated_queryset =  self.paginate_queryset(queryset)
            
        # Serialize the pagination queryset
        
        serializer = PersonSerializer(paginated_queryset, many = True)
        
        return self.get_paginated_response({'status' : 200, 'data' : serializer.data})
        # serializer = PersonSerializer(queryset,many = True)
        # return Response({'status' : 200, 'data' : serializer.data})
        
