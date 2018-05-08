$(document).ready(function() {

fetch("../profile_information/profile_update_history.json").then(rawdata=>rawdata.json()).then(data=>{
	console.log("hey")
	z=data.filter(v=>v.title && v.title.indexOf('profile picture')!=-1).sort((a,b) => b.timestamp-a.timestamp).forEach(v=>v.yr=new Date(13976391000).getFullYear())
	console.log(z);
})

    });
