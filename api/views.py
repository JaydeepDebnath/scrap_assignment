from django.shortcuts import render

from django.shortcuts import render
from .tasks import scrape_crypto_data
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from celery.exceptions import CeleryError,TaskError
from celery.result import AsyncResult

import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def start_scraping(request):
    if request.method != 'POST':
        return Response({'Error':'Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    acronyms = request.data.get('acronyms', ["DUKO", "NOT", "GORILLA"])
    if not acronyms:
        return Response({'Error': 'No acronyms provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # result = scrape_crypto_data.delay(acronyms)
        result = scrape_crypto_data.apply(args=(acronyms,))
        job_id = result.id

        scraped_data = result.get()

        tasks =[]

        for acronym in acronyms:
            task_data = {'coin':acronym,'status':'complete','output':scraped_data.get(acronym,{'Error':'Failed to fetch data'})}
            tasks.append(task_data)


        response_data = {'job_id':job_id,'tasks':tasks}
        return Response(response_data, status=status.HTTP_200_OK)
      
    except TaskError as e:
         return Response({'Error':'str(e)'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def scraping_status(request, job_id):
    try:
        job_result = AsyncResult(job_id)
        if job_result.ready():
            scraped_data = job_result.get()
            return Response(scraped_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Scraping is under progress'}, status=status.HTTP_202_ACCEPTED)
    except CeleryError as e:
        error_msg = f'Celery error:{str(e)}'
        logger.error(error_msg)
        return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        error_msg = f'An unexpected error occured:{str(e)}'
        logger.error(error_msg)
        return Response({'Error':'An unexpected error occur'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        



