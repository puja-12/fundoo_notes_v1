from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.serializers import NotesSerializer
from notes.models import Notes
import logging

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

            note = Notes.objects.get(user=request.data.get('user_id'))
            if note:

                note.title = request.data.get('title')
                note.description= request.data.get('description')
                note.save()

            return Response({'success': True,
                             'message': "Notes updated Successfully"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong", 'data': str(e)
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
