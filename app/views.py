from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DroneUserSerializer,DroneUserLoginSerializer,ImageWithDetailsSerializer, GallerySerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import  IsAdminOrReadOnly
from .models import ImageWithDetails, DroneUser, Gallery
from rest_framework.permissions import AllowAny, IsAdminUser

# Create your views here.
class DroneUserSignupView(APIView):
    permission_classes = [AllowAny]
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get(self, request):
        # Get all users excluding superusers
        users = DroneUser.objects.filter(is_superuser=False)
        context = {
            'base_url': 'https://4dkf27s7-8000.inc1.devtunnels.ms/app'
        }
        users_data = DroneUserSerializer(users, many=True, context=context).data
        
        return Response({
            "status": "success",
            "message": "Form fields and user data",
            "users": users_data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DroneUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                response_data = {
                    "status": "success",
                    "message": "User registered successfully",
                    "user_id": user.id
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DroneUserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DroneUserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Create or get the token
            token, created = Token.objects.get_or_create(user=user)

            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_superuser': user.is_superuser
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageWithDetailsViewSet(viewsets.ModelViewSet):
    queryset = ImageWithDetails.objects.all()
    serializer_class = ImageWithDetailsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add your custom base URL
        context['base_url'] = 'https://4dkf27s7-8000.inc1.devtunnels.ms/app'
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = self.get_serializer_context()
        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = self.get_serializer_context()
        serializer = self.get_serializer(instance, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['base_url'] = 'https://4dkf27s7-8000.inc1.devtunnels.ms/app'
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = self.get_serializer_context()
        serializer = self.get_serializer(queryset, many=True, context=context)
        
        return Response({
            "status": "success",
            "message": "Gallery images retrieved successfully",
            "count": len(serializer.data),
            "images": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = self.get_serializer_context()
        serializer = self.get_serializer(instance, context=context)
        
        return Response({
            "status": "success",
            "message": "Gallery image retrieved successfully",
            "image": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        if not images:
            return Response({
                "status": "error",
                "message": "No images provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        gallery_images = []
        for image in images:
            gallery = Gallery.objects.create(image=image)
            gallery_images.append(gallery)

        serializer = self.get_serializer(gallery_images, many=True)
        return Response({
            "status": "success",
            "message": f"{len(gallery_images)} images uploaded successfully",
            "images": serializer.data
        }, status=status.HTTP_201_CREATED)

