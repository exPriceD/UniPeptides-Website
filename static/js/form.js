window.onload = Animation;

var instructionFlag = "closed";

function instruction() {
    div = document.querySelector("body > div > div > form > div.instructions > div.steps");
    if (instructionFlag === "closed") {
        div.style.display = "flex";
        instructionFlag = "opened";
    } else {
        div.style.display = "none";
        instructionFlag = "closed";
    }
}
$(document).on('click', '#send', function(e) {
    e.preventDefault();
    let flag = true;
    sequenceInput = document.getElementById("sequence");
    referenceInput = document.getElementById("reference");
    if (!sequenceInput.value) {
        sequenceInput.style.border = "2px solid var(--color-red)";
        flag = false;
        sequenceInput.onfocus = function() {
            sequenceInput.style.border = "2px solid var(--color-silver)";
        }
    };
    if (!referenceInput.value) {
        referenceInput.style.border = "2px solid var(--color-red)";
        flag = false;
        referenceInput.onfocus = function() {
            referenceInput.style.border = "2px solid var(--color-silver)";
        }
    }
    if (flag) {
        startPopup('modalOkPopup');
        var form_data = new FormData();
        form_data.append('sequence', $('#sequence').val());
        form_data.append('scientific_name', $('#scientific_name').val());
        form_data.append('common_name', $("#common_name").val());
        form_data.append('activity', $("#activity").val());
        form_data.append('protein_source', $("#protein_source").val());
        form_data.append('massDa', $("#massDa").val());
        form_data.append('tissue_source', $("#tissue_source").val());
        form_data.append('pmid', $("#pmid").val());
        form_data.append('reference', $("#reference").val());

        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/database/form',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
            }
        })
        inputs = document.getElementsByClassName("input-inner");
        textarea = document.getElementById("reference");
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = ''
        };
        textarea.value = ''
    }
});