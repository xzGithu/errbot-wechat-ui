from rest_framework.decorators import api_view
from useraction.models import commands
from useraction.serializers import CommandsSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


class CommandViewSet(viewsets.ModelViewSet):
    queryset = commands.objects.all()
    serializer_class = CommandsSerializer
class MyPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"
@api_view(['GET', 'POST'])
def CommandList(request):
    '''get all commands'''
    if request.method == 'GET':
        commandsdata=commands.objects.all()
        page_list = MyPageNumberPagination()
        pg = page_list.paginate_queryset(queryset=commandsdata, request=request)
        commandsdata_serializer = CommandsSerializer(instance=pg, many=True)
        # commandsdata_serializer=CommandsSerializer(commandsdata,many=True)
        return Response(commandsdata_serializer.data)
    elif request.method == 'POST':
        serializerdata=CommandsSerializer(data=request.data)
        if serializerdata.is_valid():
            serializerdata.save()
            return Response(serializerdata.data,status=status.HTTP_200_OK)
        return Response(serializerdata.errors,status=status.HTTP_400_BAD_REQUEST)