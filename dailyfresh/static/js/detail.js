$(function(){
	var $add_x = $('#add_cart').offset().top;
	var $add_y = $('#add_cart').offset().left;

	var $to_x = $('#show_count').offset().top;
	var $to_y = $('#show_count').offset().left;
	var re_list = window.location.href.match(/\d+/g);
	var gid = re_list[re_list.length-1];

	$('#add_cart').click(function(){
		var gcount = $('.num_show').val()
		var count_sum;
		//检测登录，成功显示调加购物车动画
		if($('.login_info a').text()==''){
			location.href = '/user/login/';
			return;
		}
		$.ajax({
			async:false,
			url: '/add_' + gid + '_' + gcount + '/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function(data) {
			count_sum = data.count__sum;
		})
		.fail(function() {
			console.log("购物车添加失败");
		});
		// 动画效果
		$(".add_jump").css({'left':$add_y+70,'top':$add_x-1,'display':'block'})
		$(".add_jump").stop().animate({
			'left': $to_y-1,
			'top': $to_x-1},
			"slow", function() {
				$(".add_jump").fadeOut('fast',function(){
					$('#show_count').html(count_sum);
				});
		});
	})

	//改变数量，产生总价变化
	var price = parseFloat($('.show_pirze').html().match(/\d+\.\d+/g));
	var stock = parseInt($('.stock span').html().split('：')[1]);
	$('.add').click(function(event) {
		var count = parseInt($('.num_show').val());
		if(count<stock){
			count += 1;
		$('.num_show').val(count).keyup();
		}
	});
	$('.minus').click(function(event) {
		var n = parseInt($('.num_show').val()) - 1;
		if(n>=1){
			$('.num_show').val(n).keyup();
		}
	});
	$('.num_show').keyup(function(event) {
		var n = parseInt($(this).val());
		if(n>stock){
			$(this).val(stock).focus();
		}
		else if(n<1){
			$(this).val(1).focus()
		}
		var re = /^\d*$/g;
		if(re.test($(this).val())==0){
			$(this).val(1).focus();
		}
		n = parseInt($(this).val());
		cost = ((price*100) * (n*100)/10000).toFixed(2);
		if(cost=='NaN'){
			cost = (0).toFixed(2);
		}
		$('.total em').html(cost + '元');
	});

	$('.num_show').blur(function(event) {
		if($(this).val()==''){
			$(this).val(1).keyup().focus();
		}
	});
})