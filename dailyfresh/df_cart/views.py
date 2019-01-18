from django.shortcuts import render
from df_user.views import login_status
from django.http import JsonResponse
from .models import *
from django.db.models import Sum
from df_goods.models import *

@login_status
def cart(request):
	mycarts = CartInfo.objects.filter(user=int(request.session['user_id']))
	goods = []
	for mycart in mycarts:
		g = GoodsInfo.objects.get(pk=mycart.goods_id)
		goods.append([g, mycart.count])
	context = {
		'goods': goods,
		'doc_title': '购物车',
	}
	return render(request, 'df_cart/cart.html', context)

@login_status
def add(request, gid, gcount):
	uid = int(request.session['user_id'])
	gid = int(gid)
	gcount = int(gcount)
	# 添加购物车
	cart = CartInfo.objects.filter(user=uid, goods=gid)
	if len(cart) == 0:
		c = CartInfo()
		c.user_id = uid
		c.goods_id = gid
		c.count = gcount
		c.save()

	else:
		c = cart[0]
		c.count += gcount
		c.save()
	cart_by_user = CartInfo.objects.filter(user=uid)
	count_sum = cart_by_user.aggregate(Sum('count'))
	return JsonResponse(count_sum)

@login_status
def update(request, gid, gcount):
	try:
		mycart = CartInfo.objects.get(user=int(request.session['user_id']), goods=int(gid))
		mycart.count = int(gcount)
		mycart.save()
		status = 1
	except:
		status = 0
	return JsonResponse({'status':status})

@login_status
def delete(request, gid):
	try:
		mycart = CartInfo.objects.get(user=int(request.session['user_id']), goods=int(gid))
		mycart.delete()
		status = 1
	except:
		status = 0
	return JsonResponse({'status':status})