from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
import json
from df_cart.models import *
from django.db.models import Sum
from django.http import JsonResponse

# 装饰器：登录完成后回到之前浏览页面
def get_prelogin_page(fun):
	def get_prelogin_url(request, *args, **kwargs):
		response = fun(request, *args, **kwargs)
		response.set_cookie('url', request.get_full_path())
		return response
	return get_prelogin_url

def cart_login(fun):
	def cart_ttl(request, *args, **kwargs):
		count_sum = 0
		# 用户登录状态下，获取购物车商品数量
		if 'user_id' in request.session.keys():
			uid = int(request.session['user_id'])
			mycart = CartInfo.objects.filter(user=uid)
			count_data = mycart.aggregate(Sum('count'))
			count_sum = count_data['count__sum']
			if count_sum == None:
				count_sum = 0
		response = fun(request, count_sum, *args, **kwargs)
		return response
	return cart_ttl

@get_prelogin_page
@cart_login
def index(request, count_sum):
	list_by_id = []
	list_by_click = []
	for i in range(1,7):
		# 分别按时间和点击数排序，取前四个商品
		goods_by_id = GoodsInfo.objects.filter(gtype=i).order_by('-id')[0:4]
		goods_by_click = GoodsInfo.objects.filter(gtype=i).order_by('-gclick')[0:4]
		list_by_id.append(goods_by_id)
		list_by_click.append(goods_by_click)
	context = {
		'list_by_id': list_by_id,
		'list_by_click': list_by_click,
		'doc_title': '首页',
		'count_sum': count_sum,
	}
	response = render(request, 'df_goods/index.html', context)
	return response

@get_prelogin_page
@cart_login
def list(request, count_sum, typeid, pageid, sortid):
	# 推荐的两个最新商品
	recommend = GoodsInfo.objects.filter(gtype=typeid).order_by('-id')[0:2]
	# 根据sortid决定排序方法
	if sortid=='1':
		goods = GoodsInfo.objects.filter(gtype=typeid).order_by('id')
	elif sortid=='2':
		goods = GoodsInfo.objects.filter(gtype=typeid).order_by('gprice')
	elif sortid=='3':
		goods = GoodsInfo.objects.filter(gtype=typeid).order_by('-gclick')
	# 分页
	paginator = Paginator(goods, 10)
	page = paginator.page(int(pageid))
	context = {
		'typeid': typeid,
		'paginator': paginator,
		'page': page,
		'recommend': recommend,
		'pageid': int(pageid),
		'sortid': int(sortid),
		'doc_title': recommend[0].gtype,
		'count_sum': count_sum,
	}
	response = render(request, 'df_goods/list.html', context)
	return response

@get_prelogin_page
@cart_login
def detail(request, count_sum, gid):
	good = GoodsInfo.objects.get(pk=int(gid))
	typeid = TypeInfo.objects.get(title=good.gtype).id
	recommend = GoodsInfo.objects.filter(gtype=good.gtype).order_by('-id')[0:2]
	context = {
		'good': good,
		'recommend': recommend,
		'gcontent': json.dumps(good.gcontent, ensure_ascii=False),
		'typeid': typeid,
		'doc_title': '商品详情',
		'count_sum': count_sum,
	}
	# 打开此页面，增加点击数
	good.gclick += 1
	good.save()
	response = render(request, 'df_goods/detail.html', context)
	# 登录状态下生成浏览记录
	if 'user_id' in request.session.keys():
		record_list = json.loads(request.COOKIES.get('record_list', '[]'))
		# 判断商品id是否存在浏览记录中
		if good.id not in record_list:
			if len(record_list) < 5:
				record_list.insert(0,good.id)
			# 浏览记录大于5个，在后面追加，前面删除
			else:
				record_list.insert(0,good.id)
				record_list.pop()
		else:
			record_list.remove(good.id)
			record_list.insert(0, good.id)
		response.set_cookie('record_list', record_list)
	return response

@cart_login
def cart_count(request, count_sum):
		return JsonResponse({'count_sum': count_sum})