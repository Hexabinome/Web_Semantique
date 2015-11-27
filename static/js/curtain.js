$curtainopen = false;

function doLongCurtain()
    {
        $(this).blur();

        if ($curtainopen == false){
            $(".search").fadeOut(1000, function(){
                $(".screen").css("visibility", "visible");
                $(".screen").fadeIn(1000);

                $(this).stop().animate({top: '0px' }, {queue:false, duration:350, easing:'easeOutBounce'});
                $(".leftcurtain").stop().animate({width:'60px'}, 200000 );
                $(".rightcurtain").stop().animate({width:'60px'},200000);

            });
        }

        return false;
    };

    function doCurtain()
    {
        $(this).blur();

        if ($curtainopen == false){
            $(".search").fadeOut(1000, function(){
                /*$(".screen").css("visibility", "visible");
                $(".screen").fadeIn(1000);
                */
                $(this).stop().animate({top: '0px' }, {queue:false, duration:350, easing:'easeOutBounce'});
                $(".leftcurtain").stop().animate({width:'60px'}, 2000 );
                $(".rightcurtain").stop().animate({width:'60px'},2000 );
                $curtainopen = true;
            });
        }else{
            $(".screen").fadeOut(1000, function(){
                $(".screen").css("visibility", "hidden");
            });

            $(this).stop().animate({top: '-40px' }, {queue:false, duration:350, easing:'easeOutBounce'});
            $(".leftcurtain").stop().animate({width:'50%'}, 2000 );
            $(".rightcurtain").stop().animate({width:'51%'}, 2000 , function(){
                $(".search").fadeIn(2000);
            });
            $curtainopen = false;
        }

        return false;
    };

$(document).ready(function() {
    $(".rope").bind("click", function() {
        console.debug("rope");
        $(this).blur();

        if ($curtainopen == true){
            $(".screen").fadeOut(1000, function(){
                $(".screen").css("visibility", "hidden");
            });

            $(this).stop().animate({top: '-40px' }, {queue:false, duration:350, easing:'easeOutBounce'});
            $(".leftcurtain").stop().animate({width:'50%'}, 2000 );
            $(".rightcurtain").stop().animate({width:'51%'}, 2000 , function(){
                $(".search").fadeIn(2000);
            });
            $curtainopen = false;
        }

        return false;
    });
});

