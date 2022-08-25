from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import user
from notes.serializers import NotesSerializer
from user.models import User
from notes.models import Notes
import logging
from django.shortcuts import render

logger = logging.getLogger('django')


# Create your views here.

class NotesAPIView(APIView):

    def get(self, request):
        """
        function for getting all the notes of the user
        """
        try:

            note = Notes.objects.filter(user=request.data.get('user_id'))
            serializer = NotesSerializer(note, many=True)
            serialized_data = serializer.data

            logger.info("User successfully retrieve the data")
            return Response({'success': True,
                             'message': "Successfully retrieve the notes",
                             'data': serialized_data, }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
            function for creating notes for a particular user
        """

        try:

            serializer = NotesSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()

            logger.info("Notes created successfully")
            return Response({'success': True,
                             'message': "Notes Create Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

    def put(self, request):

        """
        function
        for updating notes for valid user
        """
        try:
            pk = request.data.get('user')
            data = Notes.objects.get(pk=pk)
            serializer = NotesSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()

            return Response({'success': True,
                             'message': "Successfully updated the notes", }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
            function for deleting note
        """
        try:
            pk = request.data.get('id')
            data = Notes.objects.get(pk=pk)
            data.delete()

            logger.info("Notes deleted successfully")
            return Response({'success': True,
                             'message': "Notes deleted successfully",
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': "Something went wrong",
                             }, status=status.HTTP_404_NOT_FOUND)
