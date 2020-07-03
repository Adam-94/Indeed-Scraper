$("#county-select").on('change', function () {
    var country_selection = $('#county-select').find("option:selected").text();
    console.log(country_selection);
    // POST
    fetch('/country-list', {

        // Specify the method
        method: 'POST',

        // JSON
        headers: {
            'Content-Type': 'application/json'
        },

        // A JSON payload
        body: JSON.stringify({
            'country_select': country_selection
        })
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST response: ');
        console.log(text);
    });

});

function search(ele) {
    if (event.key == 'Enter') {
        // POST

        var search_location = ele.value;
        fetch('/searchTextField', {

            // Specify the method
            method: 'POST',

            // JSON
            headers: {
                'Content-Type': 'application/json'
            },

            // A JSON payload
            body: JSON.stringify({
                'search_location': search_location
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
            return response.text();
        }).then(function (text) {

            console.log('POST response: ');
            console.log(text);
        });
    }
}