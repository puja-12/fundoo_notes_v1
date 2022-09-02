from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.models import Notes

from notes.serializers import NotesSerializer
from notes.utils import verify_token, RedisNoteAPI
from user.models import User
from notes.models import Notes
import logging
from django.shortcuts import render

logger = logging.getLogger('django')


# Create your views here.

class NotesAPIView(APIView):

    @verify_token
    def get(self, request):
        """
        function for getting all the notes of the user
        """
        try:

            # note = Notes.objects.filter(user=user_id)
            # serializer = NotesSerializer(note, many=True)
            # serialized_data = serializer.data
            data = RedisNoteAPI().get_note(request.data.get('user')).values()
            logger.info("User successfully retrieve the data")
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def post(self, request):
        """
            function for creating notes for a particular user
        """

        try:
            user_id = request.data.get('user')
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            RedisNoteAPI().create_note(user_id, note_id=dict(serializer.data))

            logger.info("Notes created successfully")
            return Response({'success': True,
                             'message': "Notes Create Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

    @verify_token
    def put(self, request):

        """
        function
        for updating notes for valid user
        """
        try:
            note = Notes.objects.get(pk=request.data.get('id'))
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
            function for deleting note
        """
        try:

            # pk = request.data.get('id')
            # data = Notes.objects.get(pk=pk)
            # data.delete()

            note = Notes.objects.get(id=request.data.get('id'))
            RedisNoteAPI().delete_note(request.data.get('user'), note.id)
            note.delete()

            logger.info("Notes deleted successfully")
            return Response({{'data': 'deleted'},
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'unexpected error', 'data': f"error: {e}"
                             }, status=status.HTTP_404_NOT_FOUND)
