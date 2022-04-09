function isChecked() {
    // Get the checkbox
    var checkBox = document.getElementById("checkboxNowPrice");
    // Get the input
    var text = document.getElementById("prix-add");

    var cryptoValue = document.getElementById("crypto").value;

    // If the checkbox is checked, display the output text
    if (checkBox.checked == true) {
        fetch('https://crypto-app-eval.herokuapp.com/get-data-for-js')
            .then((resp) => resp.json())
            .then(function (data) {
                data.data.map(crypto => {
                    if (crypto.symbol == cryptoValue){
                        console.log('crypto', crypto.quote.USD.price)
                        text.setAttribute('value', crypto.quote.USD.price);
                    }else {
                        console.log('aucune crypto selectionnée')
                    }
                })
            })
            .catch(function (error) {
                console.log(error);
            });

        
        text.disabled = true
    } else {
        text.setAttribute('value', '');
        text.disabled = false
    }
}


function onChangeCrypto() {

    var text = document.getElementById("prix-add");

    text.setAttribute('value', '');
    text.disabled = false
    document.getElementById("checkboxNowPrice").checked = false;


}