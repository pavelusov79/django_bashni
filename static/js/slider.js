document.addEventListener('DOMContentLoaded', function() {
    var sl = $('.slider-1');
    var fr = $('.frame_video').attr('src');
    if (sl && sl.length > 0) {
        console.log('slider-1');
        new ChiefSlider('.slider-1', {
        loop: true,
        });
    }
    if(fr && fr.length > 0) {
        console.log('slider-2');
        new ChiefSlider('.slider-2', {
            loop: true,
        });
    }
});


