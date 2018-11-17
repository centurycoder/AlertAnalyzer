function editRow(tr) {
    var td_Owner = tr.find("DIV.Owner");
    var str_Owner = td_Owner.text();
    td_Owner.text("");
    td_Owner.append('<input type="text" value="'+str_Owner+'" />');

    var td_SqlFilter = tr.find("DIV.SqlFilter");
    var str_SqlFilter = td_SqlFilter.text();
    td_SqlFilter.text("");
    td_SqlFilter.append('<input type="text" value="'+str_SqlFilter+'" />');

    var td_Button = tr.find("button");
    td_Button.first().text("save");
    // button changed to "save" means entering edit mode
    tr.addClass("editing");
}

function saveRow(tr) {
    var td_EventNameCN = tr.find("DIV.EventNameCN");
    var str_EventNameCN = td_EventNameCN.text();

    var td_Owner = tr.find("DIV.Owner");
    var str_Owner = td_Owner.find("input").val();

    var td_SqlFilter = tr.find("DIV.SqlFilter");
    var str_SqlFilter = td_SqlFilter.find("input").val();

    var dataToSave = {};
    dataToSave['Action'] = 'update'
    dataToSave['EventNameCN'] = str_EventNameCN;
    dataToSave['Owner'] = str_Owner;
    dataToSave['SqlFilter'] = str_SqlFilter;

    $.ajax({
        url: 'Setting.html',
        type: 'POST',
        data: dataToSave,
        success: function(text) {
            if (text == "SQLError") {
                alert("Illegal SQL statement !!!");
            } else if (text == "OK") {
                alert("Successfuly Saved!!!");

                td_Owner.find("input").remove();
                td_Owner.text(str_Owner);

                td_SqlFilter.find("input").remove();
                td_SqlFilter.text(str_SqlFilter);

                var td_Button = tr.find("button");
                td_Button.first().text("edit");
                // button changed to "edit" means entering save mode
                tr.removeClass("editing");
            }
        }
    });
}

function editSetting(element){
    var tr = $(element).parent().parent();
    // to edit
    if(!tr.hasClass("editing")) {
        editRow(tr);   
    } else
    // to save 
    {
        saveRow(tr);
    }
}

function addSetting(element) {
    var tr = $(element).parent().parent();
    var setting = new Array();
    tr.find("input").each(function(){
       setting.push($(this).val()); 
    })
    var dataToAdd = {};
    dataToAdd['Action'] = 'add'
    dataToAdd['EventNameCN'] = setting[0];
    dataToAdd['Owner'] = setting[1];
    dataToAdd['SqlFilter'] = setting[2];

    $.ajax({
        url: 'Setting.html',
        type: 'POST',
        data: dataToAdd,
        success: function(text) {
            if (text == "SQLError")
                alert("Illegal SQL statement !!!");
            else if (text == "AddError") 
                alert("Error when inserting data");
            else if (text =="OK") {
                alert("Successfully added");
                location.reload();
            }
        }
    });
}
