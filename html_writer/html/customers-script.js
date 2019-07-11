
log ("howdy")

$(function () {

    $('#customers').accordion({
        heightStyle: "content",
        collapsible: true,
        header:"h2.customer-header"
    })

    $('.order-list').accordion({
        heightStyle: "content",
        collapsible: true
    })

    log ("accordion called??")

});
