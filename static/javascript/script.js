let url_prod = 'https://crypto-app-eval.herokuapp.com/get-data-for-js'
let url_dev = 'http://127.0.0.1:5000/get-data-for-js'

// REGARDE SI LES CHECKBOX EST CHECK, SI OUI AFFICHE LE PRIX REEL DE LA CRYPTO SINON AFFICHE UNE ALERTE

function isChecked() {
    // Get the checkbox
    var checkBox = document.getElementById("checkboxNowPrice");
    // Get the input
    var text = document.getElementById("prix-add");
    var quantite = document.getElementById("quantite");

    var cryptoValue = document.getElementById("crypto").value;

    // If the checkbox is checked, display the output text
    if (checkBox.checked == true) {
        if(cryptoValue == 'Sélectionner une crypto' || quantite.value === ''){
            document.getElementById("alerteNoCrypto").style.display = "block";
            document.getElementById("checkboxNowPrice").checked = false;
        }else {
            fetch(url_prod)
            .then((resp) => resp.json())
            .then(function (data) {
                data.data.map(crypto => {
                    if (crypto.symbol == cryptoValue) {
                        console.log('crypto', crypto.quote.USD.price)
                        text.setAttribute('value', crypto.quote.USD.price.toFixed(2) * quantite);
                    }
                    console.log( 'text.value', text.value)
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
        }


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

var formVendre = document.getElementById("vendre");

formVendre.addEventListener('submit', e => {
    e.preventDefault();

    var quantite = document.getElementById("quantite");
    var crypto = document.getElementById("crypto");

    fetch(url_prod + '?cryptowanted=' + crypto.value)
        .then((resp) => resp.json())
        .then(function (data) {
            if(quantite.value <= data[0][0]){
                console.log('ok')
                formVendre.submit()
            }else{
                document.getElementById("alerteNoCrypto").style.display = "block";
            }
            
        })
        .catch(function (error) {
            console.log(error);
        });
});

// function validationVendre() {
//     var quantite = document.getElementById("quantite");
//     var crypto = document.getElementById("crypto");

//     let url_prod = 'https://crypto-app-eval.herokuapp.com/get-database-for-js'
//     let url_dev = 'http://127.0.0.1:5000/get-database-for-js'

//     fetch(url_dev + '?cryptowanted=' + crypto.value)
//         .then((resp) => resp.json())
//         .then(function (data) {
//             if(quantite.value <= data[0][0]){
//                 console.log('ok')
//                 return true
//             }else{
//                 document.getElementById("alerteNoCrypto").style.display = "block";
//                 return false
//             }
            
//         })
//         .catch(function (error) {
//             console.log(error);
//         });
// }
