$(function(){

	$('#login_form').submit(function() {
		var username = $('.name_input').val();
		var pwd = $('.pass_input').val();
		var name_check = false;
		var pwd_check = false;

		$.ajax({
			/*同步加载，用于修改全局变量*/
			async: false,
			url: '/user/login_check/?username='+ username + '&pwd=' + pwd,
			type: 'GET',
			dataType: 'json',
		})
		.done(function(data) {
			/*用户名匹配失败*/
			if(data.count==0){
				$('.user_error').show();
				name_check = false;
			}
			/*用户名匹配成功*/
			else{
				$('.user_error').hide();
				name_check = true;
				/*密码匹配失败*/
				if(data.pcheck==0){
					$('.pwd_error').show();
					pwd_check = false;
				}
				else{
					name_check = true;
					pwd_check = true;
				}
			}
		})
		.fail(function() {
			console.log("error：ajax加载失败！");
		});

		if(name_check == true && pwd_check == true){
			return true;
		}
		else{
			return false;
		}
	});
})
