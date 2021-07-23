
// $("#click_predict").click(clickPredict)
$("#click_back").click(clickBack)

var loadFile = function(event) {
    var image = document.getElementById('img');
    image.src = URL.createObjectURL(event.target.files[0]);
};

function clickPredict() {
    var formData = new FormData($('#myform')[0]);
    // var files = $('#file')[0].files[0];
    $.ajax({
        type:'POST',
        url: '/predict',
        data:formData,
        contentType: false,
        processData: false,
    }).done(function(response){
        debugger
    }).fail(function(response){
        debugger
    });
}

function clickBack() {
    window.location.href = 'http://0.0.0.0:5000'
}