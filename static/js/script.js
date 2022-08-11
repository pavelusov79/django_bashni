$(document).ready(function() {
    if (window.innerWidth > 475) {
        // $('.first-row-footer').children().removeClass('col-6').addClass('col-4');
        $('div.row.second-row-footer.mb-3.justify-content-center').children().removeClass('col-6').addClass('col-4');
    }
});

$('.share').on('click', function() {
    $('.share-icons').toggleClass("active");
    return false;
});

$('.type_object li').on('click', function(e) {
    $('.type_object li').each(function(e) {
        $(this).removeClass('active');
    });
    $(e.target).addClass('active');
    if ($(e.target).attr('value') == 'fl') {
        $('.block-1').css('display', 'block');
        $('.block-2').css('display', 'none');
    }else {
        $('.block-1').css('display', 'none');
        $('.block-2').css('display', 'block');
    }
});

$('.nav_modal').on('click', function(e) {
    $('.mod_btn').each(function(e) {
        $(this).removeClass('active');
    });
    $(e.target).addClass('active');
});

$('.share-item').click(function() {
    if ($('.share-menu').css('opacity') == 0) {
        $('.share-menu').css({'opacity': 1, 'transition': '1s'});
    }else if ($('.share-menu').css('opacity') == 1) {
        $('.share-menu').css({'opacity': 0, 'transition': '1s'});
    }
    return false;
});

$('.tar').click(function() {
    if($('.tar').css('font-weight', 'bold')) {
        $('.tar').css('font-weight', '100');
    }
    $(this).css('font-weight', 'bold');
});

$('#id_contact_phone').change(function () {
    var contact_phone = $('#id_contact_phone').val()
    $.ajax({
        data: {'contact_phone': contact_phone},
        url: "/property/ajax/check_phone/",
        success: function (data) {
            if (/^\+79[0-9]{9}$/.test(data['valid_phone']) !=true) {
                $('#id_contact_phone').removeClass('valid_field').addClass('invalid_field');
                $('#id_contact_phone').after('<p class="errorlist">Вводить тел. номер нужно без пробелов, скобок и дефисов в виде +79ХХХХХХХХХ</p>');
            } else {
                $('#id_contact_phone').removeClass('invalid_field').addClass('valid_field');
                $('p.errorlist').remove();
            }
        },
    });
    return false;
});

$('#sl10').slider({});

$('#sl10').on("slide", function(slideEvt) {
    $('#sl10SliderMinValue').text(slideEvt.value[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
    $('#sl10SliderMaxValue').text(slideEvt.value[1].toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
});

$('#sl7').slider({});

$('#sl7').on("slide", function(slideEvt) {
    $('#sl7SliderMinValue').text(slideEvt.value[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
    $('#sl7SliderMaxValue').text(slideEvt.value[1].toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
});

$('#sl8').slider({});

$('#sl8').on("slide", function(slideEvt) {
    $('#sl8SliderMinValue').text(slideEvt.value[0]);
    $('#sl8SliderMaxValue').text(slideEvt.value[1]);
});

$('#sl9').slider({});

$('#sl9').on("slide", function(slideEvt) {
    $('#sl9SliderMinValue').text(slideEvt.value[0]);
    $('#sl9SliderMaxValue').text(slideEvt.value[1]);
});

$('button[type="reset"]').click(function() {
    var mySlider3 = $('#sl9').slider({});
    var plugin3 = mySlider3.data('slider');
    if(plugin3) {
        plugin3.setValue([plugin3.options.min, plugin3.options.max]).refresh({useCurrentValue: true});
    $('#sl9SliderMinValue').text(plugin3.options.min);
    $('#sl9SliderMaxValue').text(plugin3.options.max);
    }
    
    var mySlider2 = $('#sl8').slider({});
    var plugin2 = mySlider2.data('slider');
    if(plugin2) {
        plugin2.setValue([plugin2.options.min, plugin2.options.max]).refresh({useCurrentValue: true});
        $('#sl8SliderMinValue').text(plugin2.options.min);
        $('#sl8SliderMaxValue').text(plugin2.options.max);
    }
    
    var mySlider1 = $('#sl7').slider({});
    var plugin1 = mySlider1.data('slider');
    if(plugin1) {
        plugin1.setValue([plugin1.options.min, plugin1.options.max]).refresh({useCurrentValue: true});
        $('#sl7SliderMinValue').text(plugin1.options.min.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
        $('#sl7SliderMaxValue').text(plugin1.options.max.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
    }
   
    var mySlider = $('#sl10').slider({});
    var plugin = mySlider.data('slider');
    if(plugin) {
        plugin.setValue([plugin.options.min, plugin.options.max]).refresh({useCurrentValue: true});
        $('#sl10SliderMinValue').text(plugin.options.min.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
        $('#sl10SliderMaxValue').text(plugin.options.max.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "));
    }
    
    $.ajax({
        type: 'GET',
        url: $('button[type="submit"]').attr('data-url'),
        data: {'reset': 1},
        success: function(response) {
            var url = window.location.href.replace(window.location.search, '');
            window.history.pushState({}, '', url);
            $('.build_class').each(function() {
                if($(this).is(':checked')) {
                    $(this).prop('checked', false);
                }
            });
            $('.build_decor').each(function() {
                if($(this).is(':checked')) {
                    $(this).prop('checked', false);
                }
            });
            $('.build_wall').each(function() {
                if($(this).is(':checked')) {
                    $(this).prop('checked', false);
                }
            });
            if($('#sort_params').val() != '') $('#sort_params option:lt(1)').remove();
            $('.flat_tp li').each(function() {
                if($(this).hasClass('active')) {
                    $(this).removeClass('active');
                }
            });
            // $('.flat_decor').each(function() {
            //     if($(this).is(':checked')) {
            //         $(this).prop('checked', false);

            //     }
            // });
            if($('select[name=finish_date]').val() != '') $('select[name=finish_date] option:lt(1)').remove();
            if($('#district').val() != '') $('#district option:lt(1)').remove();
            if($('#fl_decor').val() != '') $('#fl_decor option:lt(1)').remove();
            if($('#sort_zhk').val() != '') $('#sort_zhk').attr('value', '');
            if($('#params').val() != '') $('#params option:lt(1)').remove();
            $('#all_results').html('');
            var results = $(response).find('div.col-6.col-md-4.col-xl-3.res')
            $('#all_results').html(results);
            $('.pagination.justify-content-center').empty();
            var data = $(response).find('.pagination.justify-content-center');
            $('.pagination.justify-content-center').html(data);
            console.log('success');
        }
    });
});

$('#filter-search').click(function() {
    if($('#sort_zhk').val() != '') {
        var zhk = $('#sort_zhk').val();
    }
    // var b_class = [];
    // $('.build_class').each(function() {
    //     if($(this).is(':checked')) {
    //         b_class.push($(this).val());
    //     }
    // });
    // var decor = [];
    // $('.build_decor').each(function() {
    //     if($(this).is(':checked')) {
    //         decor.push($(this).val());
    //     }
    // });
    if($('select[name=finish_date]').val() != '') {
        var date = $('select[name=finish_date]').val();
    }

    if($('#fl_decor').val() != '') {
        var decor = $('#fl_decor').val();
    }
    // var wall = [];
    // $('.build_wall').each(function() {
    //     if($(this).is(':checked')) {
    //         wall.push($(this).val());
    //     }
    // });
    if($('#params').val() != '') {
        var param = $('#params').val()
    }

    if($('#district').val() != '') {
        var district = $('#district').val();
    }

    var firstNum = $('#sl10').attr('data-slider-min');
    var lastNum = $('#sl10').attr('data-slider-max');
    var priceVal = $('#sl10').slider({}).val();
    if(priceVal.split(',')[0] != firstNum.replace(' ', '') || priceVal.split(',')[1] != lastNum.replace(' ', '')) {
        var price = priceVal;
    }
    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {'price': price, 'param': param, 'date': date, 'decor': decor, 'district': district, 'zhk': zhk},
        success: function(response) {
            $('#all_results').html('');
            var results = $(response).find('div.col-6.col-md-4.col-xl-3.res')
            $('#all_results').html(results);
            $('.pagination.justify-content-center').empty();
            var data = $(response).find('.pagination.justify-content-center');
            $('.pagination.justify-content-center').html(data);
            console.log('success');
        }
    });
    return false;
});

$('select[name=city]').change(function() {
    var hr = $(this).val();
    window.location.href = hr;
});

/* show hide add filter */
$('.show-fil').click(function() {
    $('.show-filter').removeClass('d-flex').hide();
    $('.add-info').addClass('d-flex').show();
    $('.hide-filter').addClass('d-flex').show();
    return false;
});

$('.hide-fil').click(function() {
    $('.hide-filter').removeClass('d-flex').hide();
    $('.add-info').removeClass('d-flex').hide();
    $('.show-filter').addClass('d-flex').show();
    return false;
});

/* end */

$('#flats-search').click(function() {
    if($('#sort_zhk').val() != '') {
        var zhk = $('#sort_zhk').val();
    }

    if($('select[name=finish_date]').val() != '') {
        var date = $('select[name=finish_date]').val();
    }

    if($('#fl_decor').val() != '') {
        var fl_decor = $('#fl_decor').val();
    }
    // var fl_decor = [];
    // $('.flat_decor').each(function() {
    //     if($(this).is(':checked')) {
    //         fl_decor.push($(this).val());
    //     }
    // });
    var flat_type = [];
    $('.flat_tp li').each(function() {
        if($(this).hasClass('active')) {
            flat_type.push($(this).attr('value'));
        }
    });
    if($('#params').val() != '') {
        var param = $('#params').val();
    }

    if($('#district').val() != '') {
        var district = $('#district').val();
    }

    var firstSq = $('#sl8').attr('data-slider-min');
    var lastSq = $('#sl8').attr('data-slider-max');
    var squareVal = $('#sl8').slider({}).val();
    if(squareVal.split(',')[0] != firstSq || squareVal.split(',')[1] != lastSq) {
        var square = squareVal;
    }

    var firstNum = $('#sl7').attr('data-slider-min');
    var lastNum = $('#sl7').attr('data-slider-max');
    var priceVal = $('#sl7').slider({}).val();
    if(priceVal.split(',')[0] != firstNum || priceVal.split(',')[1] != lastNum) {
        var price = priceVal;
    }

    var firstFl = $('#sl9').attr('data-slider-min');
    var lastFl = $('#sl9').attr('data-slider-max');
    var floorVal = $('#sl9').slider({}).val();
    if(floorVal.split(',')[0] != firstFl || floorVal.split(',')[1] != lastFl) {
        var floor = floorVal;
    }

    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {'price': price, 'date': date, 'district': district, 'floor': floor, 'param': param, 'square': square, 'flat_type': flat_type.join(','), 'fl_decor': fl_decor, 'zhk': zhk},
        success: function(response) {
            $('#all_results').html('');
            var results = $(response).find('div.col-6.col-md-4.col-xl-3.res');
            $('#all_results').html(results);
            $('.pagination.justify-content-center').empty();
            var data = $(response).find('.pagination.justify-content-center');
            $('.pagination.justify-content-center').html(data);
            console.log('success');
        }
    });
    return false;
});

function ajaxPagination() {
    $('a.page-link').each(function(index, el) {
        $(el).click(function(e) {
            e.preventDefault();
            $.ajax({
                type: 'GET',
                url: $(el).attr('href'),
                success: function(response) {
                    console.log($(el).attr('href'));
                    $('#all_results').html('');
                    var results = $(response).find('div.col-6.col-md-4.col-xl-3.res');
                    $('#all_results').html(results);
                    $('.pagination.justify-content-center').empty();
                    var data = $(response).find('.pagination.justify-content-center');
                    $('.pagination.justify-content-center').html(data);
                }
            });
        });
    });
}
$(document).ready(function(){
    ajaxPagination();
});
$(document).ajaxStop(function() {
    ajaxPagination();
});

$('#likes').click(function() {
    var likes = $('#count-likes').html();
    $.ajax({
        type: 'GET',
        url: $(this).attr('data-url'),
        data: {'likes': likes},
        success: function(response) {
            $('#count-likes').html('');
            $('#count-likes').html(response.data);
            console.log('success');
        }
    });
    return false;
});

$('#comment').click(function() {
    if($('.show_comment').css('display') == 'none') {
         $('.show_comment').css('display', 'block');
    }else if($('.show_comment').css('display') == 'block') {
        $('.show_comment').css('display', 'none');
    }
});

$('#send-comment').submit(function() {
    var url = $(this).attr('action');
    $.ajax({
        type: 'POST',
        url: url,
        data: $(this).serialize(),
        success: function(response) {
            $('.show_comment').html('');
            $('.show_comment').html('Комментарий был успешно отправлен. Скоро он отобразится на сайте.');
            console.log('success');
        }
    });
    return false;
});

$('.sl4').slider({});

$('#select_num_dom').change(function() {
    var num_dom = $(this).val();
    var url = $(this).attr('action');
    console.log('num_dom= ', num_dom);
    $.ajax({
        type: 'GET',
        url: url,
        data: {'num_dom': num_dom},
        success: function(response) {
            $('.res_dom').html('');
            var results = $(response).find('div.res_dom');
            $('.res_dom').html(results);
            $('.sl4').slider({});
            console.log('success');
        }
    });
    return false;
});


$('#calc1').slider({
    tooltip: 'always'
});

// $('#calc1').on("slide", function(slideEvt) {
//     $('#calc1SliderVal').html(slideEvt.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;');
//     console.log(slideEvt.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;');
// });

$('#calc2').slider({
    tooltip: 'always'
});

$('#calc3').slider({tooltip: 'always'});
$('#calc3').slider('disable');

$('.btn-ipoteka').click(function(e) {
    e.preventDefault();
    if($('.btn-ipoteka').html() == 'Далее') {
        $('.div1').removeClass('act');
        $('.div2').addClass('act');
        $('.text-step').html('Шаг 2 из 2');
        $('.step1').css('display', 'none');
        $('.step2').css('display', 'block');
        $('.btn-ipoteka').html('Расчитать ипотеку');
    }
    else {
        $('.er-fio').css('display', 'none');
        $('.er-tel').css('display', 'none');
        var nameEl = $('input[name=fio]').val();
        var telEl = $('input[name=tel-ip]').val();
        var re = new RegExp(/^9[0-9]{9}$/);
        var re1 = new RegExp(/^[а-яА-Я]{2,}$|^[а-яА-Я]{2,}\s[а-яА-Я]{2,}$|^[а-яА-Я]{2,}\s[а-яА-Я]{2,}\s[а-яА-Я]{2,}$/);
        if (nameEl == '' || re1.test(nameEl) != true) {
            $('.er-text').append('<p class="font-italic er-fio pl-4 text-left" style="color: red;">Введите ФИО. Допускается только кирилица, не менее 2-х символов.</p>');
        }
        if (telEl == '' || re.test(telEl) != true) {
            $('.er-tel-text').append('<p class="font-italic er-tel pl-4 text-left" style="color: red;">Вводить номер нужно без пробелов начиная с 9-ки, например 9027235577 в кол-ве 10 цифр.</p>');
        }
        if (re.test(telEl) && re1.test(nameEl)) {
            var url = $('#select_num_dom').attr('action');
            $.ajax({
                type: 'POST',
                url: url,
                data: $('.ipoteka_calc_form').serialize(),
                success: function() {
                    $('.div2').removeClass('act');
                    $('.div1').addClass('act');
                    $('.text-step').html('Шаг 1 из 2');
                    $('.step2').css('display', 'none');
                    $('.step1').css('display', 'block');
                    $('.btn-ipoteka').html('Далее');
                    $('input[name=fio]').val('');
                    $('input[name=tel-ip]').val('');
                    console.log('ipoteka request was sent');
                }
            });
            return false;
        }
    }
});

// форма запроса на просмотр объекта
$('.request_form').submit(function() {
    var url = $('#select_num_dom').attr('action');
    $.ajax({
        type: 'POST',
        url: url,
        data: $(this).serialize(),
        success: function() {
            console.log('request form was sent');
            $('#modal_form_request').modal('hide');
        }
    });
    return false;
})

$(document).ready(function() {
    var val = $("#calc1Slider .slider-handle").attr('aria-valuenow');
    var val1 = $("#calc2Slider .slider-handle").attr('aria-valuenow');
    var val2 = $("#calc3Slider .slider-handle").attr('aria-valuenow');
    if (val) {
        $('#calc1Slider .tooltip-inner').html(val.replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;');
    }
    if (val1) {
        $('#calc2Slider .tooltip-inner').html(val1.replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;');
    }
    if (val2) {
        $('#calc3Slider .tooltip-inner').html(val2.replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;');
    }
});

$('#calc1').on('slide', function(slideEvt) {
    var val = $("#calc1Slider .slider-handle").attr('aria-valuenow');
    $('#calc1Slider .tooltip-inner').html(val.replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;'); 
});

$('#calc2').on('slide', function(slideEvt) {
    $('#calc2Slider .tooltip-inner').html(slideEvt.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' &#8381;') 
});

$('.type_fl').click(function(e) {
    $('.type_fl li').each(function() {
        $(this).removeClass('active');
    });
    $(e.target).addClass('active');
    var type_f = $(e.target).attr('value');
    $('.link_sale').attr('href', function(i, name) {
        return name.replace('flat_type=', `flat_type=${type_f}`);
    });
});

$('.flat_tp').click(function(e) {
    if ($(e.target).hasClass('active')) {
        $(e.target).removeClass('active');
    }else {
        $(e.target).addClass('active');
    }
});

$('#sl3').change(function() {
    var min_price = $('#sl3SliderMinValue').html() + '000000';
    var max_price = $('#sl3SliderMaxValue').html() + '000000';
    $('.link_sale').attr('href', function(i, name) {
        console.log(name.split('price')[0] + `price=${min_price}%2C${max_price}`);
        return name.split('price')[0] + `price=${min_price}%2C${max_price}`
    });
});

$('select[name=finish_date]').change(function() {
    if($('select[name=finish_date]').val() != '') {
        var date = $('select[name=finish_date]').val();
    }
    $('.link_sale').attr('href', function(i, name) {
        console.log(name.replace('date=', `date=${date}`));
        return name.replace('date=', `date=${date}`);
    });
});

$('#sl3').slider({});
$('#sl3').on("slide", function(slideEvt) {
    console.log(slideEvt.value[0]);
    $('#sl3SliderMinValue').text(slideEvt.value[0]);
    $('#sl3SliderMaxValue').text(slideEvt.value[1]);
});

$('.t_fl').click(function(e) {
    $('.t_fl li').each(function() {
        $(this).removeClass('active');
    });
    $(e.target).addClass('active');
    var t_f = $(e.target).attr('value');
    var url = $('#select_num_dom').attr('action');
    $.ajax({
        type: 'GET',
        url: url,
        data: {'type_of_flat': t_f},
        success: function(response) {
            $('.plan').html('');
            var res = $(response).find('.fl_item');
            $('.plan').html(res);
            $('.fl_pr').html('');
            var price = $(response).find('.fl_pr');
            $('.fl_pr').html(price);
            var b_img = $(response).find('.big-img img')
            $('.big-img').empty();
            $('.big-img').html(b_img);
            $('.go_sale').attr('href', function(i, name) {
                return name.replace('flat_type=1', `flat_type=${t_f}`);
            });
            console.log('success');
            $('.fl_item').click(function() {
                $('.fl_item').each(function() {
                    $(this).removeClass('div-active');
                });
                $(this).addClass('div-active');
                var src = $(this).find('>:first-child').attr('src');
                $('.big-img img').attr('src', src);
                var ind_el = $(this).index();
                var url = $('#select_num_dom').attr('action');
                var t_f = $('.t_fl li.active').attr('value');
                $.ajax({
                    type: 'GET',
                    url: url,
                    data: {'ind_el': ind_el, 'type_of_flat': t_f},
                    success: function(response) {
                        $('.fl_pr').html('');
                        var r = $(response).find('.fl_pr');
                        $('.fl_pr').html(r);
                    }
                });
                // return false;
            });
        }
    });
    return false;
});

$('.fl_item').click(function() {
    $('.fl_item').each(function() {
        $(this).removeClass('div-active');
    });
    $(this).addClass('div-active');
    var src = $(this).find('>:first-child').attr('src');
    var t_f = $('.t_fl li.active').attr('value');
    $('.big-img img').attr('src', src);
    var ind_el = $(this).index();
    var url = $('#select_num_dom').attr('action');
    $.ajax({
        type: 'GET',
        url: url,
        data: {'ind_el': ind_el, 'type_of_flat': t_f},
        success: function(response) {
            $('.fl_pr').html('');
            var res = $(response).find('.fl_pr');
            $('.fl_pr').html(res);
        }
    });
    return false;
});

$('#rating_form').change(function() {
    var url = $('#select_num_dom').attr('action');
    $.ajax({
        type: 'POST',
        url: url,
        data: $(this).serialize(),
        success: function() {
            console.log('success');
        }
    });
    return false;
});

$('.star').click(function() {
    $(this).removeClass('star').addClass('star-fill');
    $(this).nextAll().removeClass('star').addClass('star-fill');
});
