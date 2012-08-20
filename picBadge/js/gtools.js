
function get1(){



$.get("http://localhost:8000/license/api/", {name: "ggg", time: "123.00"},
   function(data){
    
    GTOOLS.log(data);
    //var ta=$('#log_text');
    //alert(ta.text());

    
    
   });
}

function post1(){

   $.post("http://localhost:8000/license/api/", {name: "ggg", time: "123.00"},
   function(data){

   GTOOLS.log(data);

   });

}

var GTOOLS={

    log:function(data){

        $('#logger').append("<div class='logr'>" + data + "</div>");
        
    },

   // $('#form_1').show('slow');$('#form_2').hide();
    showForm1:function(){
        $('#form2').hide();
        //$('#form1').show('fast');
        $('#form1').fadeIn();
        
    },
    showForm2:function(){

        $('#form1').hide();
        //$('#form2').show('fast');
        $('#form2').fadeIn();


    }
}

function init(){
    
}
