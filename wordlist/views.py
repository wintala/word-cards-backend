from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Vocabulary, WordPair
from .serializers import VocabularySerializer, WordPairsSerializer, VocabularyWithWordsSerializer
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

    def get(self, request):
        search = self.request.query_params.get("search")
        vocabs = Vocabulary.objects.filter(name__contains=search) if search else Vocabulary.objects.all().order_by("-id")[:10]
        serializer = VocabularySerializer(vocabs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VocabularyWithWordsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VocabDetail(APIView):

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
        serializer = VocabularySerializer(vocab, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vocab = self.get_object(pk)
        vocab.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WordPairList(APIView):

    def get(self, request):
        pairs = WordPair.objects.all()
        serializer = WordPairsSerializer(pairs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WordPairsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordPairDetail(APIView):

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
        serializer = WordPairsSerializer(pair, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pair = self.get_object(pk)
        pair.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)