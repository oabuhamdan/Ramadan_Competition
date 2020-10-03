function triggerDisableState(cb) {
    var field = $(cb).parent().siblings().get(0);
    if (field.classList.contains('disabled_field')) {
        field.classList.remove('disabled_field');
        $(field).find(":input:not(:checkbox)").attr('required', 'true');
    } else {
        field.classList.add('disabled_field');
        $(field).find(":input:not(:checkbox)").removeAttr('required');
    }
    $(field).find(":input")
        .val("")
        .removeAttr("checked")
        .removeAttr("selected");
    $('input[name="quran-read-pages"]').val('0')
}

$(document).ready(function () {
    $('input[type=checkbox]').prop("checked", false);
});

$('.btn-minuse').on('click', function () {
    var text_field = $(this).siblings('input')
    var text_val = parseInt(text_field.val())
    if (text_val <= 0) {
        this.setAttribute(disabled)
    } else
        text_field.val(text_val - 1)
})

$('.btn-pluss').on('click', function () {
    var text_field = $(this).siblings('input')
    var text_val = parseInt(text_field.val())
    if (text_val >= 50) {
        this.setAttribute(disabled)
    } else
        text_field.val(text_val + 1)
})
