from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 10  # Allow the client to set the page size
    max_page_size = 50  # Limit the maximum page size


class NoteAPIView(GenericAPIView):
    queryset = Note.objects.all().order_by('-id')
    serializer_class = NoteSerializer
    lookup_field = 'pk'
    pagination_class = CustomPagination


    def get(self, request, *args, **kwargs):
        try:
            instances = self.get_queryset()
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(instances, request=request, view=self)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = self.serializer_class(instances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(exception=True, data={
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = self.get_serializer(data=payload)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = serializer.data
            response_data['id'] = instance.id
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message": f'Record with id - {kwargs.get("pk")} deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
