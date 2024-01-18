# Importing the necessary modules from Django REST framework
from rest_framework import serializers

# Importing the Channel and Server models from the current module
from .models import Channel, Server

# Serializer class for the Channel model
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        # Specifying the model to be serialized (Channel) and including all fields
        model = Channel
        fields = "__all__"

# Serializer class for the Server model
class ServerSerializer(serializers.ModelSerializer):
    # Adding a custom SerializerMethodField to include 'num_members' in the serialized data
    num_members = serializers.SerializerMethodField()

    # Including a nested ChannelSerializer for the 'channel_server' field, allowing serialization of related channels
    channel_server = ChannelSerializer(many=True)

    class Meta:
        # Specifying the model to be serialized (Server) and excluding the 'member' field
        model = Server
        exclude = ("member",)
        
    # Custom method to get 'num_members' attribute for the Server instance
    def get_num_members(self, obj):
        # Checking if the 'num_members' attribute exists in the Server instance
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None
    
    # Overriding the to_representation method to customize the serialized data
    def to_representation(self, instance):
        # Calling the parent class's to_representation method to get the initial serialized data
        data = super().to_representation(instance)
        
        # Retrieving the 'num_members' value from the context
        num_members = self.context.get("num_members")
        
        # Removing the 'num_members' field from the serialized data if it is not present in the context
        if not num_members:
            data.pop("num_members", None)
        
        # Returning the final serialized data
        return data
