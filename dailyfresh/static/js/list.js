$(function(){

	var to_x = $('#show_count').offset().left;
	var to_y = $('#show_count').offset().top;
	//添加购物车点击事件
	$('.add_goods').click(function(event) {
		var count_sum;
		var gid = $(this).parent().prev().children().attr('href').match(/\d+/g);
		//检测登录，成功显示调加购物车动画
		if($('.login_info a').text()==''){
			location.href = '/user/login/';
			return;
		}
		$.ajax({
			async:false,
			url: '/add_' + gid + '_1/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function(data) {
			count_sum = data.count__sum;
		})
		.fail(function() {
			console.log("购物车添加失败");
		});
		//加入购物车动画
		var add_x = $(this).offset().left;
		var add_y = $(this).offset().top;
		$add_jump = $(this).parent().next()
		$add_jump.css({'left': add_x-15, 'top': add_y-10, 'display': 'block'});
		$add_jump.animate({'left': to_x, 'top': to_y}, 'slow', function(){
			$(this).fadeOut('fast', function() {
				$('#show_count').html(count_sum);
			});
		})
	});
})