jQuery(document).ready(function ($) {
    $('#checkAll').click(function () {
        $('input:checkbox').prop('checked', this.checked);
    });

    $("#fileSelector" ).change(function() {
        window.location.href = "/?jsonfile="+$("#fileSelector" ).val();
    });
    if ($( "textarea" ).length) {
        $("textarea").height($("textarea")[0].scrollHeight);
    }
});