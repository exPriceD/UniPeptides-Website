window.onload = Animation;

const loginInput = document.getElementById("login-input");
const passwordInput = document.getElementById("password-input");
const loginText = document.getElementById("login-helper-text");
const passwordText = document.getElementById("password-helper-text");

$(document).on('submit', '#post-form', function(e) {
    var flag = true;
    e.preventDefault();
    if (!loginInput.value) {
        flag = false;
        loginText.innerHTML = "Write your login";
        loginText.style.display = "flex";
        loginInput.style.border = "2px solid var(--color-red)";
        loginInput.onfocus = function() {
            loginText.style.display = "none";
            loginInput.style.border = "2px solid var(--gray-40)";
        }
    };
    if (!passwordInput.value) {
        flag = false;
        passwordText.innerHTML = "Write your password";
        passwordText.style.display = "flex";
        passwordInput.style.border = "2px solid var(--color-red)";
        passwordInput.onfocus = function() {
            passwordText.style.display = "none";
            passwordInput.style.border = "2px solid var(--gray-40)";
        }
    };
    if (flag === true) {
        var form_data = new FormData();
        form_data.append('login', $('#login-input').val());
        form_data.append('password', $('#password-input').val());
        form_data.append('rememberme', $('#rememberme').is(':checked'));
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/login',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log(data);
                updateStatus(data);
            }
        });
        e.stopPropagation();
    };
});

function updateStatus(data) {
    status = data["status"];
    console.log(status);
    if (status === 'User not found!') {
        loginText.innerHTML = "User not found";
        loginText.style.display = "flex";
        loginInput.style.border = "2px solid var(--color-red)";
        loginInput.onfocus = function() {
            loginText.style.display = "none";
            loginInput.style.border = "2px solid var(--gray-40)";
        }
    };
    if (status === "Incorrect password!") {
        passwordText.innerHTML = "Incorrect password";
        passwordText.style.display = "flex";
        passwordInput.style.border = "2px solid var(--color-red)";
        passwordInput.onfocus = function() {
            passwordText.style.display = "none";
            passwordInput.style.border = "2px solid var(--gray-40)";
        }
    }
    if (status === "Success!") {
        window.location.href = "/account";
    };
}