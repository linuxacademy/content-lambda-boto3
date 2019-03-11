// Set 'URL' to your API Gateway endpoint
URL = 'https://abcdefghij.execute-api.us-east-2.amazonaws.com/prod/';

$(document).ready(function () {

    $("#mainForm").submit(function (e) {
        e.preventDefault();
        
        var first_name = $("#first_name").val(),
            last_name = $("#last_name").val(),
            company = $("#company").val(),
            address1 = $("#address1").val(),
            address2 = $("#address2").val(),
            city = $("#city").val(),
            state = $("#state").val(),
            zip = $("#zip").val(),
            email = $("#email").val(),
            phone = $("#phone").val(),
            budget = $("#budget").val(),
            message = $("#message").val();

        $.ajax({
            type: "POST",
            url: URL,
            contentType: 'application/json',
            crossDomain: true, // remove in production environments
            dataType: 'json',
            // dataType: 'jsonp' // use JSONP for done() callback to work locally
            data: JSON.stringify({
                first_name: first_name,
                last_name: last_name,
                company: company,
                address1: address1,
                address2: address2,
                city: city,
                state: state,
                zip: zip,
                phone: phone,
                email: email,
                budget: budget,
                message: message
            })
        }).done(function (result) {
            console.log(result);
        }).fail(function (jqXHR, textStatus, error) {
            console.log("Post error: " + error);
            if (error != '') $('#form-response').text('Error: ' + error);
        }).always(function(data) {
            console.log(JSON.stringify(data));
            $('#form-response').text('Form submitted!');
        });

    });
});