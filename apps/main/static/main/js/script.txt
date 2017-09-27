// console.log($);
// console.log($("img"));

/* function hideImage(){
    $("img").click(function(){
        $(this).hide();
    });
}
 */
$(document).ready(function(){    
	$(".container").show();
	$('input[type="submit"]').click(function(){
		$(".container").show();
	});
});
