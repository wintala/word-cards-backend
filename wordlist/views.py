from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .models import Vocabulary, WordPair
from .serializers import VocabularySerializer, WordPairsSerializer, VocabularyWithWordsSerializer, UserSerializer

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly, IsOwnerOfVocabOrReadOnly

from rest_framework import status
from django.http import Http404

API_INFO = {"/api/vocabs": "POST, GET(list of vocabularies)",
              "/api/vocabs/<pk>": "PUT, DELETE, GET(vocabulary with word)",
              "/api/pairs": "POST, GET(list of all transalation pairs)",
              "/api/pairs/<pk>": "PUT, DELETE, GET(individual pair)"}

@api_view(['GET'])
def base(request):
    return Response(API_INFO)

class VocabList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        search = self.request.query_params.get("search")
        vocabs = Vocabulary.objects.filter(name__contains=search) if search else Vocabulary.objects.all().order_by("-id")[:10]
        serializer = VocabularySerializer(vocabs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VocabularyWithWordsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VocabDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):        
        try:
            return Vocabulary.objects.get(pk=pk)
        except Vocabulary.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        vocabs = self.get_object(pk)
        serializer = VocabularyWithWordsSerializer(vocabs, many=False)  
        return Response(serializer.data)

    def put(self, request, pk):
        vocab = self.get_object(pk)

        self.check_object_permissions(request, vocab)
            
        serializer = VocabularySerializer(vocab, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vocab = self.get_object(pk)
        self.check_object_permissions(request, vocab)
        vocab.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WordPairList(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request):
        pairs = WordPair.objects.all()
        serializer = WordPairsSerializer(pairs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WordPairsSerializer(data=request.data)
        #sanan voi lisätä vain omaan sanastoon
        self.check_object_permissions(request, Vocabulary.objects.get(pk=request.data["vocabulary"]))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordPairDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOfVocabOrReadOnly]

    def get_object(self, pk):        
        try:
            return WordPair.objects.get(pk=pk)
        except WordPair.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pair = self.get_object(pk)
        serializer = WordPairsSerializer(pair, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        pair = self.get_object(pk)
        self.check_object_permissions(request, pair)
        # foreing key ei saa muuttua
        if request.data["vocabulary"] != pair.vocabulary:
            return Response({"error": "Pair cannot be moved to another vocabulary"})
        serializer = WordPairsSerializer(pair, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pair = self.get_object(pk)
        self.check_object_permissions(request, pair)
        pair.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([AllowAny])
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        pairs = User.objects.all()
        serializer = UserSerializer(pairs, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"id": user.id, 'token': token.key}, status=status.HTTP_200_OK)
