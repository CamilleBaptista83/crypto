function isChecked() {
    // Get the checkbox
    var checkBox = document.getElementById("checkboxNowPrice");
    // Get the input
    var text = document.getElementById("prix-add");

    var crypto = document.getElementById("crypto").value;

    var myInit = {
        method: 'GET',
        headers: { 'X-CMC_PRO_API_KEY': 'da42f614-1cf8-4c99-86ff-d8aaa4a24602' }
    };

    fetch('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank', myInit)
        .then((resp) => resp.json())
        .then(function (data) {
            console.log(data)
        })
        .catch(function (error) {
            console.log(error);
        });


    // If the checkbox is checked, display the output text
    if (checkBox.checked == true) {
        text.setAttribute('value', 'My default value');
        text.disabled = true
        console.log('value', crypto)
    } else {
        text.setAttribute('value', '');
        text.disabled = false
    }
}