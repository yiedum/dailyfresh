from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
import json
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator


# 装饰器：检查用户登陆状态
def login_status(fun):
	def login_fun(request, *args, **kwargs):
		if 'user_id' in request.session.keys():
			return fun(request, *args, **kwargs)
		else:
			red = HttpResponseRedirect('/user/login/')
			red.set_cookie('url', request.get_full_path())
			return red
	return login_fun

def register(request):
	return render(request ,'df_user/register.html')

def check_uname(request):
	uname = request.GET['uname']
	count = userinfo.objects.filter(uname=uname).count()
	return JsonResponse({'count': count})

def register_handle(request):
	# 获取用户注册信息
	post = request.POST
	uname = post.get('user_name')
	upwd = post.get('pwd')
	uemail = post.get('email')
	# 密码加密
	s1 = sha1()
	s1.update(upwd.encode("utf8"))
	upwd = s1.hexdigest()
	# 用户信息存入数据库
	user = userinfo()
	user.uname = uname
	user.upwd = upwd
	user.uemail = uemail
	user.save()
	return redirect('/user/login/')

def login(request):
	# 记住用户名时，显示用户名
	cookies = request.COOKIES
	cookie_name = cookies.get('uname_remember', '')
	context = {'cookie_name': json.dumps(cookie_name, ensure_ascii=False)}
	return render(request ,'df_user/login.html', context)

def login_check(request):
	username = request.GET['username']
	pwd = request.GET['pwd']
	user = userinfo.objects.filter(uname=username)
	# 判断用户名是否正确
	count = user.count()
	pcheck = None
	# 判断密码是否正确
	if count == 1:
		s1 = sha1()
		s1.update(pwd.encode("utf8"))
		pwd = s1.hexdigest()
		pcheck = (pwd==user[0].upwd)
	return JsonResponse({'count':count, 'pcheck': pcheck})

def login_handle(request):
	post = request.POST
	uname = post.get('username')
	uid = userinfo.objects.get(uname=uname).id
	# 设置登录状态
	request.session['user_id'] = uid
	request.session['user_name'] = uname
	request.session.set_expiry(14400)
	remember = post.get('remember')
	url = request.COOKIES.get('url', '/')
	red = HttpResponseRedirect(url)
	# 设置是否记住用户名
	if remember=='on':
		red.set_cookie('uname_remember', uname)
	else:
		red.delete_cookie('uname_remember')
	return red

@login_status
def user_center_info(request):
	uid = request.session.get('user_id')
	user = userinfo.objects.filter(pk=uid)[0]
	phone, addr = user.uphone, user.uaddress
	if phone=='':
		phone = '未填写'
	if addr=='':
		addr = '未填写'
	record_list = json.loads(request.COOKIES.get('record_list', '[]'))
	goods = []
	if record_list != []:
		for rid in record_list:
			good = GoodsInfo.objects.get(pk=rid)
			goods.append(good)
	context = {
		'name': user.uname,
		'phone': phone,
		'addr': addr,
		'doc_title': '用户中心',
		'goods': goods,
	}
	return render(request, 'df_user/user_center_info.html', context)

@login_status
def user_center_order(request, pid):
	orders = OrderInfo.objects.filter(user=int(request.session['user_id']))
	myorders = []
	for o in orders:
		ods = OrderDetail.objects.filter(order=o.oid)
		goodses = []
		myorders.append([o, goodses])
		for od in ods:
			goods = GoodsInfo.objects.get(pk=od.goods_id)
			goodses.append([goods, od.oprice, od.ocount])
	paginator = Paginator(myorders, 2)
	page = paginator.page(pid)
	context = {
		'doc_title': '我的订单',
		'orders': page,
		'paginator': paginator,
	}
	return render(request, 'df_user/user_center_order.html', context)

@login_status
def user_center_site(request):
	uid = request.session.get('user_id')
	# 遇到post请求，上传用户信息
	user = userinfo.objects.filter(pk=uid)[0]
	if request.method=='POST':
		post = request.POST
		user.ushou = post['shou']
		user.uaddress = post['addr']
		user.uphone = post['phone']
		user.save()
	# 显示用户信息
	context = {'user': user, 'doc_title': '收货地址'}
	return render(request, 'df_user/user_center_site.html', context)

def logout(request):
	request.session.flush()
	return redirect('/')





