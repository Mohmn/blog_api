from rest_framework import serializers
from .models import Blog,Author



class AuthorSerializer(serializers.ModelSerializer):

    author_socialDetails = ['followers','following']

    class Meta:
        model = Author
        fields = ('username','followers','following','email','password','profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        return Author.objects.create(**validated_data)

    def update(self,instance,validated_data):
        
        # for attr,value in validated_data.items():
        for action in self.author_socialDetails:
            if action in validated_data:
                values = validated_data.pop(action)
                
                if action == "followers":
                    for user in values:
                        instance.followers.add(user)
                        user.following.add(instance)
                else:
                    for user in values:
                        instance.following.add(user)
                        user.followers.add(instance)

        # for values other than  ['followers','following']  
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Blog
        fields = '__all__'