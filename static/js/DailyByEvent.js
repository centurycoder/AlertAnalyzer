function editEvent(element){
    var ButtonCell = jQuery(element).parent();
    var InputCell = ButtonCell.prev();


    if (!InputCell.hasClass("editing")) {
        InputCell.addClass("editing");
        var value = jQuery(InputCell).text();
        jQuery(InputCell).text("");
        jQuery(InputCell).append('<input type="textarea" value="'+value+'" />');
        jQuery(element).text("save");

    } else {
        InputCell.removeClass("editing");
        var value = jQuery(InputCell).find("input").val();
        jQuery(InputCell).text(value);
        jQuery(InputCell).find("input").remove();
        jQuery(element).text("edit");

        var Row = ButtonCell.parent();
        var EventNameCN = Row.children().first().text();
        var day=$('#WhichDay')[0].value;
        jQuery.post("/DailyByEvent.html",{"day":day,"EventNameCN":EventNameCN,"input":value})
    };
}
