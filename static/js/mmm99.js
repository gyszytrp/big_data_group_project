//window.alert("JS TEST!")
function success(){
    window.alert("Submit success!")
}

function talkToThisPerson( obj ) {
    document.getElementById("talk_person").innerText = obj.innerText;
    var value=obj.innerText;
    fetch('gettarget?value=' + value)
	.then(function(response) {
	    return response.text();
	})
	.then(function(text) {
	    console.log(text);
	    output.innerText = text;
	});
}

function buttonTrigger() {
    var value=""
    var output = document.getElementById('messageTextarea');
    value=value+output.value
    // output.innerText = 'Button clicked, waiting for response...';

    fetch('getmessage?value=' + value)
        .then(function(response) { 
            return response.text();
        })
        .then(function(text) {
            console.log(text);
            output.innerText = text;
        });
}
function sendMessage(obj) {
    var messageTextareaNode = document.getElementById("messageTextarea");
    //  if(messageTextareaNode.value.trim() == ""){
    //     alert("message is empty");
    //     return ;
    // }
    var addStr = "            <div class=\"m-right\">\n" +
        "                <span>"+ messageTextareaNode.value +"</span>\n" +
        "            </div>";
    messageTextareaNode.value = "";
    var messageShowPaneNode = document.getElementById("messageShowPane");
    messageShowPaneNode.innerHTML = messageShowPaneNode.innerHTML + addStr;
}
