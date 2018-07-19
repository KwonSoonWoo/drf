from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Snippet
from .serializers import SnippetSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # many=True -> 여러개를 한번에 시리얼라이징 하겠다
        serializer = SnippetSerializer(snippets, many=True)
        # serializer.data가 파이썬 데이터가 str형식으로 받는거라 json형식으로 변환
        json_data = JSONRenderer().render(serializer.data)
        # content_type -> postman에서 데이터를 읽을때 어떤 형식으로 읽을지 알려주는것
        # 기본은 HTML
        return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'POST':
        data = JSONParser().parse(request.POST)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.data, status=400)
