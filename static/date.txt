$(document).ready(function(){
	wtf = new Date();
	wtf_date = wtf.getDate()+'/'+(wtf.getMonth()+1)+'/'+wtf.getFullYear();
	$('#datepicker').val(wtf_date)
	$('#datepicker').datepicker({value:''+wtf_date,format:'d/m/Y'});
})