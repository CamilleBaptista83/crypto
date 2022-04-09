// REGARDE SI LES CHECKBOX EST CHECK, SI OUI AFFICHE LE PRIX REEL DE LA CRYPTO SINON AFFICHE UNE ALERTE

function isChecked() {
    // Get the checkbox
    var checkBox = document.getElementById("checkboxNowPrice");
    // Get the input
    var text = document.getElementById("prix-add");

    var cryptoValue = document.getElementById("crypto").value;

    let url_prod = 'https://crypto-app-eval.herokuapp.com/get-data-for-js'
    let url_dev = 'http://127.0.0.1:5000/get-data-for-js'

    // If the checkbox is checked, display the output text
    if (checkBox.checked == true) {
        fetch(url_dev)
            .then((resp) => resp.json())
            .then(function (data) {
                data.data.map(crypto => {
                    if (crypto.symbol == cryptoValue){
                        console.log('crypto', crypto.quote.USD.price)
                        text.setAttribute('value', crypto.quote.USD.price.toFixed(2));
                    }
                    // else {
                    //     text.setAttribute('value', '');
                    //     text.disabled = false
                    //     document.getElementById("alerteNoCrypto").style.display = "block";
                    //     document.getElementById("checkboxNowPrice").checked = false;
                    // }
                })
            })
            .catch(function (error) {
                console.log(error);
            });

        
        // text.disabled = true
    } else {
        text.setAttribute('value', '');
        text.disabled = false
    }
}


//SUPPRIME LE CHECK DE LA CHEKBOX SI ON CHANGE DE CRYPTO ETRE TEMPS

function onChangeCrypto() {

    var text = document.getElementById("prix-add");

    text.setAttribute('value', '');
    text.disabled = false
    document.getElementById("checkboxNowPrice").checked = false;


}
