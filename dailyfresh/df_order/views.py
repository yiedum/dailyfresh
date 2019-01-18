from django.shortcuts import render, redirect
from df_user.views import login_status
from df_user.models import userinfo
from df_goods.models import GoodsInfo
from df_cart.models import CartInfo
from django.http import JsonResponse
from .models import *
import datetime
import re
from django.db import transaction

@login_status
def order(request):
	gid_list = request.GET.getlist('gid')
	user = userinfo.objects.get(pk=int(request.session['user_id']))
	carts = []
	for gid in gid_list:
		goods = GoodsInfo.objects.get(pk=int(gid))
		mycart = CartInfo.objects.get(user=user.id, goods=int(gid))
		carts.append([goods, mycart.count])
	context = {
		'carts': carts,
		'user': user,
		'doc_title': '提交订单',
	}
	return render(request, 'df_order/place_order.html', context)

@transaction.atomic
@login_status
def order_submit(request):
	tran_id = transaction.savepoint()
	post = request.POST
	gids = post.getlist('gids[]')
	t = ''.join(re.findall('\d+', str(datetime.datetime.now())))
	try:
		o = OrderInfo()
		o.oid = t
		o.user_id = int(request.session['user_id'])
		o.ocost = float(post.get('cost'))
		o.save()
		for gid in gids:
			goods = GoodsInfo.objects.get(pk=int(gid))
			cart = CartInfo.objects.get(user=o.user_id, goods=int(gid))
			if cart.count <= goods.gstock:
				goods.gstock -= cart.count
				goods.save()
			else:
				transaction.savepoint_rollback(tran_id)
				return redirect('/cart/')
			od = OrderDetail()
			od.goods_id = int(gid)
			od.order_id = o.oid
			od.oprice = goods.gprice
			od.ocount = cart.count
			od.save()
			cart.delete()
		status = 1
	except Exception as e:
		print(e)
		transaction.savepoint_rollback(tran_id)
		status = 0
	return JsonResponse({'status': status})


