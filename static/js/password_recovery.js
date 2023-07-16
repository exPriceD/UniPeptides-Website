window.onload = Animation;

const emailInput = document.getElementById("email-input");
const emailText = document.getElementById("email-helper-text");

function checkEmail() {
    if (!(emailInput === document.activeElement) && emailInput.value.length > 0 && !emailInput.value.includes('@')) {
        emailText.innerHTML = "Invalid email";
        emailText.style.display = "flex";
        emailInput.style.border = "2px solid var(--color-red)";
    } else {
        emailText.style.display = "none";
        emailInput.style.border = "2px solid var(--gray-40)";
    }
    if (!(emailInput === document.activeElement) && emailInput.value.includes('@') && emailInput.value.length > 0) {
        emailInput.style.border = "2px solid #115424";
    }
}
var intervalEmail = setInterval(checkEmail, 100);
setInterval(intervalEmail, 100);

$(document).on('submit', '#post-form', function(e) {
    e.preventDefault();
    if (!emailInput.value) {
        clearInterval(intervalEmail);
        emailText.innerHTML = "Write your email";
        emailText.style.display = "flex";
        emailInput.style.border = "2px solid var(--color-red)";
        emailInput.onfocus = function() {
            intervalEmail = setInterval(checkEmail, 100);
            emailText.style.display = "none";
            emailInput.style.border = "2px solid var(--gray-40)";
            setInterval(intervalEmail, 100);
        }
        return;
    }
    var form_data = new FormData();
    form_data.append('email', $("#email-input").val());
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/password_recovery',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log(data);
            updateStatus(data);
        }
    })
});

function updateStatus(data) {
    status = data['status']
    if (status === 'Failed') {
        emailText.innerHTML = "User not found";
        emailText.style.display = "flex";
        emailInput.style.border = "2px solid var(--color-red)";
        clearInterval(intervalEmail);
        emailInput.onfocus = function() {
            intervalEmail = setInterval(checkEmail, 100);
            emailText.style.display = "none";
            emailInput.style.border = "2px solid var(--gray-40)";
            setInterval(intervalEmail, 100);
        }
        return;
    }
    if (status === 'Success') {
        document.getElementById('instruction').style.display = "flex";
    }

}