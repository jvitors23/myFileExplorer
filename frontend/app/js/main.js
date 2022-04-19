const LOGOUT_URL = "/api/user/logout/";
const SIGNUP_URL = "/api/user/signup/";
const TOKEN_URL = "/api/user/token/";
const TOKEN_REFRESH_URL = "/api/user/token/refresh/"
const INDEX_URL = "/";
const BASE_URL = "https://3.234.194.198.nip.io";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
