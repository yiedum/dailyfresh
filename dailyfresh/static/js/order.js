$(function(){
	var count_ttl = 0;
	var cost_ttl = 0;
	$('.col07').each(function() {
		var price = parseFloat($(this).siblings('.col05').html());
		var count = parseInt($(this).prev().html());
		var cost_sum = (price*100)*(count*100)/10000;
		$(this).html(cost_sum.toFixed(2)+'元');
		count_ttl += count;
		cost_ttl += cost_sum;

	});
	$('.total_goods_count em').html(count_ttl);
	$('.total_goods_count b').html(cost_ttl.toFixed(2)+'元');
	$('.total_pay b').html((cost_ttl+10).toFixed(2)+'元');

	/*var csrftoken = document.cookie.match(/csrftoken=\w+/g)[0].split('=')[1];*/
	var csrftoken = $("[name='csrfmiddlewaretoken']").val();
	$('#order_btn').click(function() {
		var args = location.href.split('/');
		var gids = args[args.length-1].match(/\d+/g);
		var cost = (cost_ttl+10).toFixed(2)
		$.post('/order_submit/', {
			'cost': cost,
			'gids': gids,
			'csrfmiddlewaretoken': csrftoken
		}, function(data) {
			if(data.status==1){
				$('.popup_con').fadeIn('fast', function(){
					setTimeout(function(){
						location.href = '/cart/';
					}, 1000)
				});
			}
			else{
				$('.popup p').html('订单提交失败！');
				$('.popup p').css({'color':'red'});
				$('.popup_con').fadeIn('fast', function(){
					setTimeout(function(){
						$('.popup_con').fadeOut('fast')
					}, 1000)
				})
			}			
		});
	});
})
