window.onload = Animation;


var selectedFlag = false;

function selectAll() {
    checkbox = document.getElementsByClassName('checkbox');
    if (!selectedFlag) {
        for (let i = 0; i < checkbox.length; i++) {
            checkbox[i].checked = true;
        }
        selectedFlag = true;
    } else {
        for (let i = 0; i < checkbox.length; i++) {
            checkbox[i].checked = false;
        }
        selectedFlag = false;
    }
}

function downloadSelected() {
    var form_data = new FormData();
    checkbox = document.getElementsByClassName('checkbox');
    for (let i = 0; i < checkbox.length; i++) {
        if (checkbox[i].checked) {
            parent_id = checkbox[i].parentElement.id;
            form_data.append(parent_id, 'true');
        }
        if (form_data) {
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: '/account/download',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    console.log("success");
                }
            });
        }
    }
}

function removeResult(result_id) {
    result = document.getElementById(result_id);
    result.remove();
    var form_data = new FormData();
    form_data.append('id', result_id);
    if (form_data) {
        console.log(result_id);
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/account/remove',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log("success");
            }
        });
    }
}