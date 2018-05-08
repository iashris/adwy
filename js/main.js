// Fetch profile photo

fetch("../profile_information/profile_update_history.json").then(rawdata=>rawdata.json()).then(data=>{
	var selected = data.filter(function (v) {
		console.log(v);
		if (v.title) {
			return v.title.indexOf('perfil') != -1 || v.title.indexOf('profile') != -1
		} else {
			return false;
		}
	})
	console.log(selected)
	$('#mepic').attr('src', selected.sort((a, b) => b.timestamp - a.timestamp)[0].attachments[0].data[0].media.uri);
})

