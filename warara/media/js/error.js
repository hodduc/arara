$(document).ready(function(){
        $("#error_alert").hide();
        if($("#error_alert").text() == "NOT_LOGGED_IN"){
        $("#error_notice").hide();
        alert("not loggen in");
        history.go(-1);
        }
        if($("#error_alert").text() == "ALREADY_LOGGED_IN"){
        $("#error_notice").hide();
        alert("already loggen in");
        location.href = "/main";
        }
		});
