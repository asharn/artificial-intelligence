var outputArea = $("#chat-output");

$("#user-input-form").on("submit", function(e) {
  
  e.preventDefault();
  
  var message = $("#user-input").val();
  
  outputArea.append(`
    <div class='bot-message'>
      <div class='message'>
        ${message}
      </div>
    </div>
  `);
  
  setTimeout(function() {
	$.ajax(
		{
			type: "POST",
			url: "/nlu_parsing",
			data: JSON.stringify({"utterance":message}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
	
				outputArea.append(`
						<div class='bot-message'>
						  <div class='message'>
						  ${JSON.stringify(data)}
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