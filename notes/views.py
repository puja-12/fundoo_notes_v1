from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.serializers import NotesSerializer
from notes.utils import verify_token

from notes.models import Notes
import logging
from rest_framework.serializers import ValidationError

logger = logging.getLogger('django')


# Create your views here.

class NotesAPIView(APIView):

    @verify_token
    def get(self, request):
        """
        function for getting all the notes of the user
        """
        try:
            user_id = request.data.get('user')
            note = Notes.objects.filter(user=user_id)

            serializer = NotesSerializer(note, many=True)
            serialized_data = serializer.data

            logger.info("User successfully retrieve the data")
            return Response({'success': True,
                             'message': "Successfully retrieve the notes",
                             'data': serialized_data, }, status=status.HTTP_200_OK)


        except ValidationError as e:
            return Response({'success': False,
                             'message': e.detail
                             }, status=status.HTTP_400_BAD_REQUEST)

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

            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            logger.info("Notes created successfully")
            return Response({'success': True,
                             'message': "Notes Create Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'success': False,
                             'message': e.detail
                             }, status=status.HTTP_400_BAD_REQUEST)

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


            note = Notes.objects.get(pk=request.data.get('id'))
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': True,
                             'message': "Notes updated Successfully"},
                            status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'success': False,
                             'message': e.detail
                             }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong", 'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
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
            return Response({'success': False, 'message': "Something went wrong", 'data': f"error: {e}"
                             }, status=status.HTTP_404_NOT_FOUND)
