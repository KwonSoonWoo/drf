import json
import random

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snippet


class SnippetListTest(APITestCase):
    """
    Snippet List요청에 대한 테스트
    """
    URL = '/snippets/generic_cbv/snippets/'

    def test_snippet_list_status_code(self):
        """
        요청 결과의 HTTP상태코드가 200인지 확인
        :return:
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_list_count(self):
        """
        Snippet List를 요청시 DB에 있는 자료수와 같은 갯수로 리턴되는지 테스트
            response (self.client.get요청 한 결과)에 온 데이터의 길이와
            Django ORM을 이용한 QuerySet의 갯수가
                같은지 확인

            response.content에 ByteString타입의 JSON String이 들어있음
            테스트시 임의로 몇 개의 Snippet을 만들고 진행 (테스트DB는 초기화된 상태로 시작)
        :return:
        """
        for i in range(random.randint(10, 100)):
            Snippet.objects.create(code=f'a = {i}')
        response = self.client.get(self.URL)
        data = json.loads(response.content)

        # response로 받은 JSON데이터의 길이와
        # Snippet테이블의 자료수(COUNT)가 같은
        self.assertEqual(len(data), Snippet.objects.count())

    def test_snippet_list_order_by_created_descending(self):
        """
        Snippet List의 결과가 생성일자 내림차순인지 확인
        :return:
        """
        for i in range(random.randint(5, 10)):
            Snippet.objects.create(code=f'a = {i}')
        response = self.client.get(self.URL)
        data = json.loads(response.content)
        # snippets = Snippet.objects.order_by('-created')
        #
        # # response에 전달된 JSON string을 파싱한 Python 객체를 순회하며 'pk'값만 꺼냄
        # data_pk_list = []
        # for item in data:
        #     data_pk_list.append(item['pk'])
        #
        #
        # # Snippet.objects.order_by('-created') QuerySet을 순회하며 각 Snippet인스턴스의 pk값만 꺼냄
        # snippets_pk_list = []
        # for snippet in snippets:
        #     snippets_pk_list.append(snippet.pk)

        self.assertEqual(
            # JSON으로 전달받은 데이터에서 pk만 꺼낸 리스트
            [item['pk'] for item in data],
            # DB에서 created역순으로 pk값만 가져온 QuerySet으로 만든 리스트
            list(Snippet.objects.order_by('-created').values_list('pk', flat=True))
        )


CREATE_DATA = '''{
	"code": "print('hello, world')"
}'''


class SnippetCreatetest(APITestCase):
    URL = '/snippets/generic_cbv/snippets/'

    def test_snippet_create_status_code(self):
        """
        201이 들어오는지
        :return:
        """
        # 실제 JSON형식 데이터를 전송
        # response = self.client.post(
        #     '/snippets/django_view/snippets/',
        #     data=CREATE_DATA,
        #     content_type='application/json',
        # )

        response = self.client.post(
                self.URL,
                data={
                    'code': "print('hello, world')",
                },
                format='json',
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_snippet_create_save_db(self):
        """
        요청 후 실제 DB에 저장되었는지
        :return:
        """
        # 생성할 Snippet에 사용될 정보
        snippet_data = {
            'title': 'SnippetTitle',
            'code': 'SnippetCode',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }

        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        # snippet_detail내의 키들을 동적으로 순회하면서 아래코드를 실행
        # (for문으로 바꾸기)
        # response로 받은 데이터와 Snippet생성시 사용한 데이터가 같은지 확인
        for key in snippet_data:
            self.assertEqual(data[key], snippet_data[key])
        # self.assertEqual(data['title'],snippet_data['title'])
        # self.assertEqual(data['code'],snippet_data['code'])
        # self.assertEqual(data['linenos'],snippet_data['linenos'])
        # self.assertEqual(data['language'],snippet_data['language'])
        # self.assertEqual(data['style'],snippet_data['style'])

    def test_snippet_create_missing_code_raise_exception(self):
        """
        'code'데이터가 주어지지 않을 경우 적절한 Exception이 발생하는지
        :return:
        """

        # code만 주어지지 않은 데이터
        snippet_data = {
            'title': 'SnippetTitle',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }
        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json',
        )

        # code가 주어지지 않으면 HTTP상태코드가 400이어야 함
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

