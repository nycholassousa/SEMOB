function get_current_url() {
    var url=window.location.href;
    return url
}

$(window).on('load',function(){
    var current_url=document.getElementsByClassName('current_url')[0];
    current_url.value=get_current_url();
})