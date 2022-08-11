document.addEventListener('DOMContentLoaded', function() {
    new ChiefSlider('.slider-1', {
        loop: true,
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var fr = $('.frame_video').attr('src');
    if(fr) {
        new ChiefSlider('.slider-2', {
            loop: true,
        });
    }   
});
