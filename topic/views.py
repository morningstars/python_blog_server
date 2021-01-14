import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from tools.logging_decorator import logging_check
from topic.models import Topic
from user.models import UserProfile


# Create your views here.

@logging_check('POST', 'GET')
def topics(request, author_id=None):
    if request.method == 'POST':
        # 发表博客

        # 当前token中认证通过的用户即为作者
        author = request.user

        # 没有使用表单提交  使用request.body  取数据
        # 使用form表单提交  使用request.POST.get 取数据
        json_str = request.body

        if not json_str:
            result = {'code': 301, 'error': 'Please post data'}
            return JsonResponse(result)

        json_obj = json.loads(json_str)

        title = json_obj.get('title')
        content = json_obj.get('content')
        content_text = json_obj.get('content_text')
        introduce = content_text[:30]

        limit = json_obj.get('limit')
        if limit not in ['public', 'private']:
            result = {'code': 303, 'error': 'Please give right limit!'}
            return JsonResponse(result)

        category = json_obj.get('category')
        if category not in ['tec', 'no-tec']:
            result = {'code': 304, 'error': 'Please give right category!'}
            return JsonResponse(result)

        now = datetime.datetime.now()

        try:
            Topic.objects.create(
                title=title,
                content=content,
                limit=limit,
                category=category,
                introduce=introduce,
                author=author,
                create_time=now,
                modify_time=now
            )
            result = {'code': 200, 'username': author.username}
            return JsonResponse(result)
        except Exception as e:
            print('error is %s' % e)
            result = {'code': 305, 'error': 'Create error'}
            return JsonResponse(result)

    elif request.method == 'GET':

        author = request.user

        topics = Topic.objects.all()

        if not topics:
            result = {'code': 306, 'error': 'Have no blog'}
            return JsonResponse(result)

        result = {'code': 200,
                  'data': {
                      'nickname': 'hello'
                  }}
        topic_list = []
        for t in topics:
            print(t.create_time)
            dic = {'id': t.id,
                   'title': t.title,
                   'categoty': t.category,
                   # 'create_time': '{yyyy-MM-dd hh:mm:ss}'.format(t.create_time),
                   'content': t.content,
                   'introduce': t.introduce,
                   'author': t.author.username
                   }
            topic_list.append(dic)

        result['data']['topics'] = topic_list
        return JsonResponse(result)


