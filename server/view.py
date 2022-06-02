from django.http import JsonResponse
from django.views import View

from db_util import redis_conn


class GetProxy(View):
    def get(self, request):
        proxy = redis_conn.zrevrangebyscore('proxy', -100, 100)[0]
        proxy = proxy.decode(encoding='utf-8')
        return JsonResponse({
            'data': proxy
        })
