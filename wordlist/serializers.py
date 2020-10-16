from rest_framework import serializers
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
        fields = ("id", "name", "wordpairs")
    
    def create(self, validated_data):
        pairs = validated_data.pop("wordpairs")
        vocabulary = Vocabulary.objects.create(**validated_data)
        for pair in pairs:
            WordPair.objects.create(**pair, vocabulary=vocabulary)
        return vocabulary

