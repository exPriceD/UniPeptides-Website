window.onload = Animation;

const pass1 = document.getElementById("password-input1");
const pass2 = document.getElementById("password-input2");
const pass1Text = document.getElementById("pass1-helper-text");
const pass2Text = document.getElementById("pass2-helper-text");
const url = window.location.href;

$(document).on('submit', '#post-form', function(e) {
    e.preventDefault();
    msg = document.getElementById('instruction');
    msg.style.display = 'none';
    if (!pass1.value) {
        pass1Text.innerHTML = "Write your password";
        pass1Text.style.display = "flex";
        pass1.style.border = "2px solid var(--color-red)";
        pass1.onfocus = function() {
            pass1Text.style.display = "none";
            pass1.style.border = "2px solid var(--gray-40)";
        }
        return;
    }
    if (!pass2.value) {
        pass2Text.innerHTML = "Repeat your password";
        pass2Text.style.display = "flex";
        pass2.style.border = "2px solid var(--color-red)";
        pass2.onfocus = function() {
            pass2Text.style.display = "none";
            pass2.style.border = "2px solid var(--gray-40)";
        }
        return;
    }

    if (pass1.value != pass2.value) {
        pass2Text.innerHTML = "Passwords don't match";
        pass2Text.style.display = "flex";
        pass2.style.border = "2px solid var(--color-red)";
        pass1.style.border = "2px solid var(--color-red)";
        pass2.onfocus = function() {
            pass2Text.style.display = "none";
            pass2.style.border = "2px solid var(--gray-40)";
            pass1.style.border = "2px solid var(--gray-40)";
        }
        pass1.onfocus = function() {
            pass2Text.style.display = "none";
            pass2.style.border = "2px solid var(--gray-40)";
            pass1.style.border = "2px solid var(--gray-40)";
        }
        return;
    }

    var form_data = new FormData();
    form_data.append('pass1', $("#password-input1").val());
    form_data.append('pass2', $("#password-input2").val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: url,
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log(data);
            updateStatus(data);
        }
    })
    e.stopPropagation();
});

function updateStatus(data) {
    status = data['status'];
    if (status === 'Success') {
        msg = document.getElementById('instruction');
        msg_text = document.getElementById('msg_text');
        msg_text.innerHTML = 'The password has been changed';
        msg.style.display = "flex";
    } else {
        msg = document.getElementById('instruction');
        msg_text = document.getElementById('msg_text');
        msg.classList.add('red');
        msg_text.innerHTML = 'Unexpected error';
        msg.style.display = "flex";
    }
}