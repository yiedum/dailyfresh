from django.db import models

class OrderInfo(models.Model):
	oid = models.CharField(max_length=20, primary_key=True)
	user = models.ForeignKey('df_user.userinfo', on_delete=models.CASCADE)
	odate = models.DateTimeField(auto_now=True)
	ocost = models.DecimalField(max_digits=6, decimal_places=2)
	ispay = models.BooleanField(default=False)

class OrderDetail(models.Model):
	order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
	goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
	oprice = models.DecimalField(max_digits=5, decimal_places=2)
	ocount = models.IntegerField()

