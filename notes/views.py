import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions


from notes.models import Notes
from notes.serializers import NotesSerializer, ShareNoteSerializer, NoteLabelSerializer
from notes.utils import verify_token
from user.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger('django')


# Create your views here.

class NotesAPIView(generics.GenericAPIView):

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, "token", type=openapi.TYPE_STRING)
    ])
    @verify_token
    def get(self, request):
        """
        function for getting all the notes of the user
        """
        try:
            look_ups = Q(user=request.data.get('user')) | Q(collaborator__id=request.data.get("user"))

            notes = Notes.objects.filter(look_ups).order_by("-is_pinned")
            logger.info("User successfully retrieve the data")
            return Response({"data": NotesSerializer(notes, many=True).data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, "token", type=openapi.TYPE_STRING)
    ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    @verify_token
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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, "token", type=openapi.TYPE_STRING)
    ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
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

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, "token", type=openapi.TYPE_STRING)
    ],

    )
    @verify_token
    def delete(self, request, id):
        """
            function for deleting note
        """
        try:

            data = Notes.objects.get(pk=id)
            data.delete()

            return Response({'data': 'deleted'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'unexpected error', 'data': f"error: {e}"
                             }, status=status.HTTP_404_NOT_FOUND)


class NoteLabelAPIView(APIView):

    @verify_token
    def post(self, request):
        """
           creating label for user
           """

        try:
            label = Notes.objects.get(id=request.data.get("id"))
            serializer = NoteLabelSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data)
            return Response({
                "message": "label found", "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        delete label of user
        """
        try:
            data = get_object_or_404(Labels, id=request.data.get("labels"))
            note = get_object_or_404(Notes, id=request.data.get("id"))
            note.labels.remove(data)

            return Response({'data': 'deleted'}
                            , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CollaboratorAPIView(APIView):

    @verify_token
    def post(self, request):
        """
        Add a new note
        """
        try:
            note = Notes.objects.get(id=request.data.get("id"))
            serializer = ShareNoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "user found", "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        delete note of user
        """
        try:

            data = get_object_or_404(User, id=request.data.get("user_id"))
            note = get_object_or_404(Notes, id=request.data.get("id"))
            note.collaborator.remove(data)

            return Response({'data': 'deleted'}
                            , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PinnedNotes(APIView):

    def put(self, request, *args, **kwargs):
        try:

            id = self.kwargs.get("id")
            note_id = id
            note = Notes.objects.get(id=note_id)
            if not note.is_pinned:
                note.is_pinned = True
                note.save()
                return Response({'data': 'is pinned'}, status=status.HTTP_200_OK)

            elif note.is_pinned:
                note.is_pinned = False
                note.save()
                return Response({'data': ' unpinned'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



