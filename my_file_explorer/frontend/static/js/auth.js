var loginForm = document.getElementById('login-form');
var usernameInput = document.getElementById('id_username')
var passwordInput = document.getElementById('id_password')
var errorMessage = document.getElementById('error-messages')

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    var requestData = {
        headers: {
            Accept: "application/json",
            "Content-Type": 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        method: "POST",
        body: JSON.stringify({
            username: usernameInput.value,
            password: passwordInput.value,
        })
    }
    function handleError(){
        errorMessage.innerText = "Login failed! Check your credentials!"
    }
    fetch(LOGIN_URL, requestData)
        .then(response => {
            if(response.status != 200){
                handleError()
            }
            window.location.href = INDEX_URL;
        })
        .catch(error => {
            handleError()
        });
});
