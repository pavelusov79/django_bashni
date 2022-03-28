var phone = $('.phone');
if (window.innerWidth < 900) {
    phone.html('<i class="fa fa-phone fa-lg fa-nav" style="color: #1A284C;" aria-hidden="true"></i>');
}

$(document).ready(function() {
    if (window.innerWidth > 475) {
        $('.first-row-footer').children().removeClass('col-6').addClass('col-4');
        $('div.row.second-row-footer.mb-3.justify-content-center').children().removeClass('col-6').addClass('col-4');
    }
});

$('.share').on('click', function() {
    $('.share-icons').toggleClass("active");
    return false;
});

$('.tar').click(function() {
    if($('.tar').css('font-weight', 'bold')) {
        $('.tar').css('font-weight', '100');
    }
    $(this).css('font-weight', 'bold');
});

$('#id_contact_phone').keyup(function () {
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

$('.ex2').slider({});
$('button[type="reset"]').click(function() {
    var mySlider = $('.ex2').slider({});
    var plugin = mySlider.data('slider')
    plugin
            .setValue([plugin.options.min, plugin.options.max])
            .refresh({useCurrentValue: true});
    $.ajax({
        type: 'GET',
        url: $('button[type="submit"]').attr('data-url'),
        data: {'reset': 1},
        success: function(response) {
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
            $('.flat_type').each(function() {
                if($(this).is(':checked')) {
                    $(this).prop('checked', false);
                    console.log('checkbox flat_type was unchecked');
                }
            });
            $('.flat_decor').each(function() {
                if($(this).is(':checked')) {
                    $(this).prop('checked', false);

                }
            });
            if($('#sort_zhk').val() != '') $('#sort_zhk option:lt(1)').remove();
            if($('#params').val() != '') $('#params option:lt(1)').remove();
            window.location.href.replace(window.location.search, '');
            $('#all_results').html('');
            var results = $(response).find('div.col-6.col-md-4.res')
            $('#all_results').html(results);
            $('.pagination.justify-content-center').empty();
            var data = $(response).find('.pagination.justify-content-center');
            $('.pagination.justify-content-center').html(data);
            console.log('success');
        }
    });
});

$('#filter-search').click(function() {
    var b_class = [];
    $('.build_class').each(function() {
        if($(this).is(':checked')) {
            b_class.push($(this).val());
        }
    });
    var decor = [];
    $('.build_decor').each(function() {
        if($(this).is(':checked')) {
            decor.push($(this).val());
        }
    });
    var wall = [];
    $('.build_wall').each(function() {
        if($(this).is(':checked')) {
            wall.push($(this).val());
        }
    });
    if($('#sort_params').val() != '') {
        var param = $('#sort_params').val()
    }
    var firstNum = $('.initial-val').html().slice(0, -2);
    var lastNum = $('.final-val').html().slice(0, -2);
    var priceVal = $('.ex2').slider({}).val();
    if(priceVal.split(',')[0] != firstNum.replace(' ', '') || priceVal.split(',')[1] != lastNum.replace(' ', '')) {
        var price = priceVal;
    }
    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {'price': price, 'param': param, 'b_class': b_class.join(','), 'decor': decor.join(','), 'wall': wall.join(',')},
        success: function(response) {
            $('#all_results').html('');
            var results = $(response).find('div.col-6.col-md-4.res')
            $('#all_results').html(results);
            $('.pagination.justify-content-center').empty();
            var data = $(response).find('.pagination.justify-content-center');
            $('.pagination.justify-content-center').html(data);
            console.log('success');
        }
    });
    return false;
});

$('#flats-search').click(function() {
    if($('#sort_zhk').val() != '') {
        var zhk = $('#sort_zhk').val();
    }
    var fl_decor = [];
    $('.flat_decor').each(function() {
        if($(this).is(':checked')) {
            fl_decor.push($(this).val());
        }
    });
    var flat_type = [];
    $('.flat_type').each(function() {
        if($(this).is(':checked')) {
            flat_type.push($(this).val());
        }
    });
    if($('#params').val() != '') {
        var param = $('#params').val();
    }
    var firstNum = $('.initial-val').html().slice(0, -2);
    var lastNum = $('.final-val').html().slice(0, -2);
    var priceVal = $('.ex2').slider({}).val();
    if(priceVal.split(',')[0] != firstNum.replace(' ', '').replace(' ', '') || priceVal.split(',')[1] != lastNum.replace(' ', '').replace(' ', '')) {
        var price = priceVal;
    }
    var url = $(this).attr('data-url');
    $.ajax({
        type: 'GET',
        url: url,
        data: {'price': price, 'param': param, 'flat_type': flat_type.join(','), 'fl_decor': fl_decor.join(','), 'zhk': zhk},
        success: function(response) {
            $('#all_results').html('');
            var results = $(response).find('div.col-6.col-md-4.res');
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
                    var results = $(response).find('div.col-6.col-md-4.res');
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

