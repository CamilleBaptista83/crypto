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
		if (cryptoValue == "Sélectionner une crypto" || quantite.value === "") {
			document.getElementById("alerteNoCrypto").style.display = "block";
			document.getElementById("checkboxNowPrice").checked = false;
		} else {
			fetch(window.url)
				.then((resp) => resp.json())
				.then(function (data) {
					data.data.map((crypto) => {
						if (crypto.symbol == cryptoValue) {
							document.getElementById(
								"alerteNoCrypto"
							).style.display = "none";
							console.log("crypto", crypto.quote.USD.price);
							prix_total =
								crypto.quote.USD.price * quantite.value;
							text.setAttribute("value", prix_total.toFixed(2));
						}
						console.log("text.value", text.value);
						// else {
						//     text.setAttribute('value', '');
						//     text.disabled = false
						//     document.getElementById("alerteNoCrypto").style.display = "block";
						//     document.getElementById("checkboxNowPrice").checked = false;
						// }
					});
				})
				.catch(function (error) {
					console.log(error);
				});
		}
	} else {
		text.setAttribute("value", "");
		text.disabled = false;
	}
}

//SUPPRIME LE CHECK DE LA CHEKBOX SI ON CHANGE DE CRYPTO ETRE TEMPS

function onChangeCrypto() {
	var text = document.getElementById("prix-add");

	text.setAttribute("value", "");
	text.disabled = false;
	document.getElementById("checkboxNowPrice").checked = false;
}

var formVendre = document.getElementById("vendre");

formVendre.addEventListener("submit", (e) => {
	e.preventDefault();

	var quantite = document.getElementById("quantite");
	var crypto = document.getElementById("crypto");

	fetch(window.url + "?cryptowanted=" + crypto.value)
		.then((resp) => resp.json())
		.then(function (data) {
			if (quantite.value <= data[0][0]) {
				console.log("ok");
				formVendre.submit();
			} else {
				document.getElementById("alerteNoCrypto").style.display =
					"block";
			}
		})
		.catch(function (error) {
			console.log(error);
		});
});
