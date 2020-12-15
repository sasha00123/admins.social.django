$(document).ready(function () {
    $('.chart-head a').click(function (e) {
        e.preventDefault();
        $('.chart-head .active').removeClass('active');
        $(this).addClass('active');
        var tab = $(this).attr('href');
        $('.tab').not(tab).css({'display': 'none'});
        $(tab).fadeIn(400);
    });
});

/*
$(document).ready(function () {
    $('#menu-content li').click(function (e) {
        e.preventDefault();
        $('#menu-content .active').removeClass('active');
        $(this).addClass('active');
    });
});
*/


function getUserData() {
    if (Cookies.get('logged_in') === true) {
        return Cookies.get('userData');
    }
    return {
        "first_name": "Алексей",
        "last_name": "Русаков",
        "subscriptions": [],
        "profile": {
            "avatar": "https://pp.userapi.com/c604820/v604820494/4071b/0nkMSnZB_JE.jpg?ava=1",
            "groups": [
                104193245,
                169486555,
                169493004,
                169492992,
                169492977,
                169445982,
                169492963,
                169445891,
                169420888
            ]
        }
    }
}

function GraphqlQueryPromise(query) {
    return axios.post("/api/graphql", query);
}

function afterLogin() {
    Cookies.set('logged_in', true);
    Cookies.set('userData', getUserData());
}

function afterLogout() {
    Cookies.remove('logged_in');
    Cookies.remove('userData');
}

function isLoggedIn() {
    return Cookies.get('logged_in') === true;
}

function serialize(obj) {
    var str = [];
    for (var p in obj)
        if (obj.hasOwnProperty(p)) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }
    return str.join("&");
}
