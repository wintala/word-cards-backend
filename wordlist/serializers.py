from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WordPair, Vocabulary



class WordPairsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordPair
        fields = "__all__"


class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = "__all__"


class WordPairsSerializerNested(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = WordPair
        fields = "__all__"
        read_only_fields = ["vocabulary"]

class VocabularyWithWordsSerializer(serializers.ModelSerializer):
    wordpairs = WordPairsSerializerNested(many=True)

    class Meta:
        model = Vocabulary
        fields = ("id", "name", "wordpairs", "owner")
    
    def create(self, validated_data):
        pairs = validated_data.pop("wordpairs")
        vocabulary = Vocabulary.objects.create(**validated_data)
        for pair in pairs:
            WordPair.objects.create(**pair, vocabulary=vocabulary)
        return vocabulary

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user