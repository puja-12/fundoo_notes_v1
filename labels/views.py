import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.utils import verify_token

from labels.models import Labels
from labels.serializers import LabelSerializer

logger = logging.getLogger('django')


class LabelAPIView(APIView):
    @verify_token
    def get(self, request):
        """
        function for getting all the labels of the user
        """
        try:

            label = Labels.objects.all()
            serializer = LabelSerializer(label, many=True)
            serialized_data = serializer.data

            logger.info("User successfully retrieve the data")
            return Response({'success': True,
                             'message': "Successfully retrieve the labels",
                             'data': serialized_data, }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def post(self, request):
        """
            function for creating labels for a particular user
        """

        try:

            serializer = LabelSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()

            logger.info("labels created successfully")
            return Response({'success': True,
                             'message': "labels Create Successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)


    @verify_token
    def delete(self, request,id):
        """
        function for deleting label
        """
        try:

            data = Labels.objects.get(pk=id)
            data.delete()
            return Response({'success': True,
                             'message': 'Successfully Deleted Data',
                             }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'success': False,
                             'message': 'Something went wrong',
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)