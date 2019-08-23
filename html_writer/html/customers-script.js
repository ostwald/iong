
log ("howdy from customer-script")


slog (PARAMS)

log (window.location)

var filename = window.location.pathname.split('/').slice (-1);

log ('filename: ' + filename)

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

    $("#title-bar button.nav")
        .button()
        .click (function (event) {
            var filename = window.location.pathname.split('/').slice (-1);
            var view = window.location.pathname.split('/').slice (-2, -1);
            log ('view: ' + view);
            var href = null;
            if (view == "customer_email") {
                href = "../customer_name/"+filename;
            } else if (view == "customer_name") {
                href = "../customer_email/"+filename;
            }
            log (href)
            window.location = href;
        })

});
