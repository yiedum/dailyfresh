$(function(){

	var $check_singles = $(':checkbox:not(#check_all)');
	//全选全消，重新计算计算选中数量
	$('#check_all').click(function() {
		var ischecked = $('#check_all').prop('checked');
		$check_singles.prop('checked', ischecked);
		ttl();
	});

	//单体选择，重新计算计算选中数量
	$check_singles.click(function(){
		var $checked_singles = $(':checked:not(#check_all)');
		if($checked_singles.length == $check_singles.length){
			$('#check_all').prop('checked', true);
		}
		else{
			$('#check_all').prop('checked', false);
		}
		ttl();
	});

	// 小计
	cost_sum();
	// 总计
	ttl();

	// 加减数量，页面变动
	$('.add').click(function() {
		var count = $(this).next().val();
		var stock1 = $(this).parents('.col06').siblings('.col03').find('b').html();
		if(parseInt(count)<parseInt(stock1)){
			$(this).next().val(parseInt($(this).next().val())+1).blur();
		}
	});
	$('.minus').click(function() {
		var count1 = $(this).prev().val();
		if(parseInt(count1)>1){
			$(this).prev().val(parseInt($(this).prev().val())-1).blur();
		}
	});

	// 数据库更新购物车数据
	$('.num_show').blur(function() {
		var gid = $(this).parents('.cart_list_td').attr('id');
		var gcount = $(this).val();
		var stock = $(this).parents('.col06').siblings('.col03').find('b').html();
		// 限制数量的格式和范围
		var re = /^\d+$/g;
		if(re.test(gcount)==0){
			$(this).val(1).focus();
			gcount = 1;
		}
		gcount = parseInt($(this).val());
		if(gcount<1){
			$(this).val(1).focus();
			gcount = 1;
		}
		if(gcount>parseInt(stock)){
			$(this).val(stock).focus();
			gcount = parseInt(stock);
		}
		$.get('/update_' + gid + '_' + gcount + '/', function(data) {
			if(data.status==1){
				ttl();
			}
			else{
				$(this).focus();
			}
		});
		cost_sum();
	});

	// 数据库删除购物车数据
	$('.cart_list_td .col08 a').click(function() {
		var gid = $(this).parents('.cart_list_td').attr('id');
		$.get('/delete_' + gid + '/', function(data) {
			if(data.status==1){
				$('ul').remove('#'+gid);
				ttl();
				if($('ul').length < 3){
					location.reload();
				}
			}	
		});
	});

	// 费用小计
	function cost_sum(){   
		$('.cart_list_td .col07').each(function() {
			var count2 = $(this).prev().find('.num_show').val();
			var price = $(this).prev().prev().html();
			cost = (parseFloat(price)*100)*(parseFloat(count2)*100)/10000;
			$(this).html(cost.toFixed(2));
		})
	};

	// 商品总数，勾选的费用总计，勾选的商品总计
	function ttl(){
		// 商品总数
		var count_sum1 = 0;
		$('.num_show').each(function() {
			var count3 = $(this).val();
			count_sum1 += parseInt(count3);
		});
		$('.total_count em').html(count_sum1);
		$('#count_ttl').html(count_sum1);
		
		var cost_ttl_checked = 0;
		var count_sum_checked = 0;
		var url = '/order/?';
		if($(':checked:not(#check_all)').length==0){
			url = 'javascript:;';
		}
		else{
			$(':checked:not(#check_all)').each(function(index) {
				// 勾选的商品总价
				var cost = parseFloat($(this).parent().siblings('.col07').html());
				cost_ttl_checked += cost;
				// 勾选的商品总数
				var count4 = $(this).parent().siblings('.col06').find('.num_show').val();
				count_sum_checked += parseInt(count4);
				// 修改结算处href
				var gid = $(this).parents('.cart_list_td').attr('id');
				if(index==0){
					url += ('gid='+gid);
				}
				else{
					url += ('&gid='+gid);
				}
			});
		}

		$('#cost_ttl').html(cost_ttl_checked.toFixed(2));
		$('#count_ttl').html(count_sum_checked);
		$('#settle').attr('href', url);
	};
})