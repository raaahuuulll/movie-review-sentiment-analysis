$(document).ready(function(){
    $("#submit").click(function(){
        $("#result").innerHTML="";
        var review = $("#review").val();
        $.ajax({
            type:"POST",
            url:"/predict",
            data:{
                "review":review
            },
            success: function(result){
                var resultElement = document.getElementById('result');
                if(result['status']==1){
                    if(result['prediction']==1){
                        resultElement.className = 'bg-success';
                        resultElement.innerHTML = 'Your review was POSITIVE!';
                    } else if(result['prediction']==0) {
                        resultElement.className = 'bg-danger';
                        resultElement.innerHTML = 'Your review was NEGATIVE!';
                    } else {
                        resultElement.className = '';
                        resultElement.innerHTML = '';
                    }
                } else {
                    resultElement.className = 'bg-info';
                    resultElement.innerHTML = result['message'];
                }
                console.log(result);
            }
        });
        document.getElementById('review').value = "";
    });

    $("#reset").click(function(){
        var resultElement = document.getElementById('result');
        var textArea = document.getElementById('review');
        resultElement.innerHTML = "";
        textArea.value = "";
    });
});
