import axios from 'https://cdn.skypack.dev/axios';

export const api = axios.create({
    baseURL: BASE_URL,
});

if(getCookie('access_token')){
    api.defaults.headers.authorization = `Bearer ${getCookie('access_token')}`;
}

api.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');

axios.interceptors.response.use(response => {
    return response;
}, err => {
    if(err.response.status === 401){
        if(getCookie('refresh_token')){
            api.post(TOKEN_REFRESH_URL, {

            });
        }else{
            window.location.href = LOGIN_URL;
        }
    }
});
