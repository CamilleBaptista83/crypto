// REGARDE SI LES CHECKBOX EST CHECK, SI OUI AFFICHE LE PRIX REEL DE LA CRYPTO SINON AFFICHE UNE ALERTE
if(jQuery('#form-add').length){
    jQuery('#form-add').submit(function(e){
        e.preventDefault();
        if(
            jQuery('#crypto').val() == '' || jQuery('#quantite').val() == '' || parseFloat(jQuery('#quantite').val()) < 0
        ){
            jQuery('#alerteNoCrypto').show();
            jQuery('#checkboxNowPrice').prop('checked', false);
        }else{
            e.currentTarget.submit();
        }
    });
}

function isChecked() {
    if (jQuery('#checkboxNowPrice').is(':checked')) {
        if(
            jQuery('#crypto').val() == '' || jQuery('#quantite').val() == '' || parseFloat(jQuery('#quantite').val()) < 0
        ){
            jQuery('#alerteNoCrypto').show();
            jQuery('#checkboxNowPrice').prop('checked', false);
        }else{
            jQuery.getJSON(url_api,function(resp){
                jQuery(resp.data).each(function(key, crypto){
                    if (crypto.symbol == jQuery('#crypto').val()) {
                        jQuery('#alerteNoCrypto').hide();
                        let prix_total = parseFloat(crypto.quote.USD.price) * parseFloat(jQuery('#quantite').val());
                        jQuery('#prix-add').val(prix_total.toFixed(2))
                    }
                });
            })
        }
    } else {
		jQuery('#prix-add').val("").prop('disabled', false);
	}
}

//SUPPRIME LE CHECK DE LA CHEKBOX SI ON CHANGE DE CRYPTO ETRE TEMPS

function onChangeCrypto() {
    jQuery('#prix-add').val("").prop('disabled', false);
    jQuery('#checkboxNowPrice').prop('checked', false);
}

if(jQuery('#vendre').length){
    jQuery('#vendre').submit(function(e){
        e.preventDefault();
        if(
            jQuery('#crypto').val() == '' || jQuery('#quantite').val() == '' || parseFloat(jQuery('#quantite').val()) < 0
        ){
            jQuery('#alerteNoCrypto').show();
            jQuery('#checkboxNowPrice').prop('checked', false);
        }else{
            jQuery.getJSON(url_api_one, { "cryptowanted" : jQuery('#crypto').val() },function(data){
                if (parseFloat(jQuery('#quantite').val()) <= data[0][0]) {
                    e.currentTarget.submit();
                } else {
                    jQuery('#alerteNoCrypto').show();
                }
            })
        }
    });
}