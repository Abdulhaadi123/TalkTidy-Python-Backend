from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .services import GroqService
from .models import PresentationFeedback
from .utils import (
    extract_ppt_content,
    extract_docx_content,
    extract_text_content,
    format_content_for_llm
)
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class FeedbackView(APIView):
    def post(self, request):
        logger.info(f"Received request data: {request.data}")
        logger.info(f"Received files: {request.FILES}")

        content_type = request.data.get('type', 'text')
        content = request.data.get('content')
        file = request.FILES.get('file')

        if not content and not file:
            return Response(
                {'error': 'Either content or file must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        groq_service = GroqService()

        try:
            if content_type == 'file' and file:
                # Check file type
                file_name = file.name.lower()
                if not (file_name.endswith(('.ppt', '.pptx', '.doc', '.docx', '.txt'))):
                    return Response(
                        {'error': 'Unsupported file type. Please upload a PowerPoint (.ppt/.pptx), Word (.doc/.docx), or text (.txt) file'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

          
                file_path = default_storage.save(f'presentations/{file.name}', file)
                full_path = default_storage.path(file_path)
                
                try:
                    
                    if file_name.endswith(('.ppt', '.pptx')):
                        extracted_content = extract_ppt_content(full_path)
                        file_type = 'ppt'
                    elif file_name.endswith(('.doc', '.docx')):
                        extracted_content = extract_docx_content(full_path)
                        file_type = 'docx'
                    else: 
                        extracted_content = extract_text_content(full_path)
                        file_type = 'txt'
                    
             
                    formatted_content = format_content_for_llm(extracted_content, file_type)
                    
                    feedback = groq_service.get_presentation_feedback(formatted_content)
                    
                   
                    presentation_feedback = PresentationFeedback.objects.create(
                        content=formatted_content,
                        feedback=feedback,
                        content_type='file',
                        file_path=file_path
                    )
                    
                    return Response({
                        'id': presentation_feedback.id,
                        'feedback': feedback,
                        'created_at': presentation_feedback.created_at
                    }, status=status.HTTP_201_CREATED)
                    
                finally:
                    
                    if os.path.exists(full_path):
                        os.remove(full_path)
            else:
                
                if not content:
                    return Response(
                        {'error': 'Text content is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                feedback = groq_service.get_presentation_feedback(content)
                
               
                presentation_feedback = PresentationFeedback.objects.create(
                    content=content,
                    feedback=feedback,
                    content_type='text'
                )

                return Response({
                    'id': presentation_feedback.id,
                    'feedback': feedback,
                    'created_at': presentation_feedback.created_at
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Error processing request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
