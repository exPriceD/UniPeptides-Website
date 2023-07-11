window.onload = Animation;
const loginInput = document.getElementById("login-input");
const emailInput = document.getElementById("email-input");
const passwordInput = document.getElementById("password-input");
const loginText = document.getElementById("login-helper-text");
const emailText = document.getElementById("email-helper-text");
const passwordText = document.getElementById("password-helper-text");

function checkLength() {
    if (loginInput.value.length > 16) {
        loginText.innerHTML = "The username is too long. Maximum 16 characters";
        loginText.style.display = "flex";
        loginInput.style.border = "2px solid var(--color-red)";
    } else {
        loginText.style.display = "none";
        loginInput.style.border = "2px solid var(--gray-40)";
    }
    if (!(loginInput === document.activeElement) && loginInput.value.length < 16 && loginInput.value.length > 0) {
        loginInput.style.border = "2px solid #115424";
    }
}

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
var intervalLogin = setInterval(checkLength, 100);
var intervalEmail = setInterval(checkEmail, 100);
loginInput.onfocus = function() {
    setInterval(intervalLogin, 100);
}
setInterval(intervalEmail, 100);

$(document).on('submit', '#post-form', function(e) {
    e.preventDefault();
    var flag = true;
    if (!loginInput.value) {
        flag = false;
        clearInterval(intervalLogin);
        loginText.innerHTML = "Write your login";
        loginText.style.display = "flex";
        loginInput.style.border = "2px solid var(--color-red)";
        loginInput.onfocus = function() {
            intervalLogin = setInterval(checkLength, 100);
            loginText.style.display = "none";
            loginInput.style.border = "2px solid var(--gray-40)";
            setInterval(intervalLogin, 100);
        }
    };
    if (!emailInput.value) {
        flag = false;
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
        form_data.append('username', $('#login-input').val());
        form_data.append('email', $('#email-input').val());
        form_data.append('password', $('#password-input').val());
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/register',
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
    }
});
function updateStatus(data) {
    status = data["status"];
    console.log(status);
    if (status === 'Username already exist!') {
        clearInterval(intervalLogin);
        loginText.innerHTML = "User already exist";
        loginText.style.display = "flex";
        loginInput.style.border = "2px solid var(--color-red)";
        loginInput.onfocus = function() {
            intervalLogin = setInterval(checkLength, 100);
            loginText.style.display = "none";
            loginInput.style.border = "2px solid var(--gray-40)";
            setInterval(intervalLogin, 100);
        };
    };
    if (status === "Email already exist!") {
        clearInterval(intervalEmail);
        emailText.innerHTML = "Email already exist";
        emailText.style.display = "flex";
        emailInput.style.border = "2px solid var(--color-red)";
        emailInput.onfocus = function() {
            intervalEmail = setInterval(checkEmail, 100);
            emailText.style.display = "none";
            emailInput.style.border = "2px solid var(--gray-40)";
            setInterval(intervalEmail, 100);
        };
    }
    if (status === "Success!") {
        window.location.href = "/account";
    };
}