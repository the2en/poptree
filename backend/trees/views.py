from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TreeStatus
from .serializers import TreeStatusSerializer
from .utils import update_tree_status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tree_status(request):
    user = request.user
    update_tree_status(user)
    tree_status = TreeStatus.objects.get(user=user)
    serializer = TreeStatusSerializer(tree_status)
    return Response(serializer.data)
