# Importing Count aggregation function from Django models
from django.db.models import Count
# Importing necessary components from Django REST framework
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

# Importing the Server model and ServerSerializer from the current module
from .models import Server
from .schema import server_List_docs
from .serializers import ServerSerializer


# ViewSet class for handling Server list-related operations
class ServerListViewSet(viewsets.ViewSet):
    
    # Initial queryset containing all Server objects
    queryset = Server.objects.all()
    
    # Custom 'list' method to handle GET requests for the Server list
    @server_List_docs
    def list(self, request):
        """
        Handles the GET request to retrieve a list of servers with optional filtering.

        This method processes the incoming HTTP request, applies optional filters based on query parameters,
        and returns a serialized response containing the server data.

        Args:
        request (rest_framework.request.Request): The incoming HTTP request.

        Returns:
        rest_framework.response.Response: The serialized response containing the server data.

        Raises:
        rest_framework.exceptions.AuthenticationFailed:
        If the query requires user authentication, and the request user is not authenticated.
        This exception is raised for queries that involve user-specific data.

        rest_framework.exceptions.ValidationError:
        If there are validation errors during parameter processing. This includes cases
        where the provided parameters are not in the expected format or violate certain constraints.

        ValueError:
        If an unexpected error occurs during the handling of the 'by_serverid' parameter.
        This could be caused by incorrect data types or unexpected values.

        Note:
        This method supports the following query parameters:

        - 'category' (str): Filters servers by category name.
        - 'qty' (int): Limits the number of servers returned.
        - 'by_user' (bool): Filters servers by the authenticated user (requires authentication).
        - 'with_num_members' (bool): Includes the count of members for each server in the response.
        - 'by_serverid' (int): Filters servers by the specified server ID.

        Example:
        To retrieve a list of servers in a specific category:
        ```
        GET /servers/?category=example_category
        ```

        To limit the response to 5 servers:
        ```
        GET /servers/?qty=5
        ```

        To retrieve servers by the authenticated user:
        ```
        GET /servers/?by_user=true
        ```

        For more information on available query parameters, refer to the API documentation.
        """
        
        
        # Extracting query parameters from the request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"
        
        # Checking authentication for queries that require user authentication
        
        # Filtering queryset based on the 'category' parameter
        if category:
            self.queryset = self.queryset.filter(category__name=category)
            
        # Filtering queryset based on the authenticated user, if specified
        if by_user:
            if by_user and not request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()
            
        # Annotating queryset with the count of members, if 'with_num_members' is specified
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Limiting queryset results based on the 'qty' parameter
        if qty:
            self.queryset = self.queryset[: int(qty)]
            
        # Filtering queryset based on the 'by_serverid' parameter and handling exceptions
        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail="Server value error")
            
        # Serializing the queryset and returning the response
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
