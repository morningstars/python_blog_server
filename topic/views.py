import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from tools.logging_decorator import logging_check
from tools.logging_decorator import get_user_by_request
from topic.models import Topic
from user.models import UserProfile


# Create your views here.

@logging_check('POST')
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
        # v1/topics/zhangsan
        # 获取用户博客列表 / 具体的博客内容【带 ?t_id=xxx 】

        # 访问当前博客的访问者 --visitor   --author
        author = UserProfile.objects.filter(username=author_id).first()

        if not author:
            result = {'code': 306, 'error': 'The current author is not exist'}
            return  JsonResponse(result)

        visitor = get_user_by_request(request)

        # 判断两个的username是否一致  从而判断是否要获取private的博客
        visitor_username = None
        if visitor:
            visitor_username = visitor.username

        if visitor_username == author_id:
            # 博主在访问自己的博客
            author_topics = Topic.objects.filter(author_id=author_id)
        else:
            # 其他访问者在访问当前博客
            author_topics = Topic.objects.filter(author_id=author_id, limit='public')

        result = make_topics_res(author, author_topics)
        return JsonResponse(result)


def make_topics_res(author, author_topics):
    result = {'code': 200, 'data': {}}
    topic_list = []
    for topic in author_topics:
        print(topic.create_time)
        dic = {
            'id': topic.id,
            'title': topic.title,
            'categoty': topic.category,
            'created_time': topic.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'content': topic.content,
            'introduce': topic.introduce,
            'author': topic.author.nickname
        }
        topic_list.append(dic)

    result['data']['topics'] = topic_list
    result['data']['nickname'] = author.nickname
    return result
