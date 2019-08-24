var outputArea = $("#chat-output");

$("#user-input-form").on("submit", function(e) {
  
  e.preventDefault();
  
  var message = $("#user-input").val();
  
  outputArea.append(`
    <div class='user-message'>
      <div class='message'>
	  User: ${message}
      </div>
    </div>
  `);
  
  setTimeout(function() {
	$.ajax(
		{
			type: "POST",
			url: "/nlu_parsing",
			data: JSON.stringify({"user-utter":message}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log(data);
				outputArea.append(`
						<div class='bot-message'>
						  <div class='message'>
						  Bot: ${data.intent.name}
						  </div>
						</div>
					  `);
			},
			error: function (msg, url, line) {
				alert('msg = ' + msg + ', url = ' + url + ', line = ' + line);
	
			}
		});
      }, 250);
  
  $("#user-input").val("");
  
});