
function ac(retdata) {
     //window.foo = retdata;
     $(retdata).each( function() {
         $(".actors_concept").append("<h2> Actors from concept </h2><ul id='results-" + "'></ul>");
         $(this.actors).each(function(){
             $('#results-').append(
                     '<li>' + this[0] + ', ' + this[1] + '</li>' );
            });
    });
};

function abc(retdata) {
    //window.foo = retdata;
    $(".actors_broaders_concept").append("<h2> Actors from broaders of concept </h2>");
    $(retdata).each( function() {
        var broader = this.broader;
        var broader_dom = broader.replace(/,/g,"").replace(/ /g,"");
        $(".actors_broaders_concept").append("<h4>" + broader + "</h4><ul id='results-" + broader_dom + "'></ul>");
        $(this.actors).each(function(){
            $('#results-'+broader_dom).append(
                    '<li>' + this[0] + ', ' + this[1] + '</li>' );
            });
    });
};


function anc(retdata) {
    //window.foo = retdata;
    $(".actors_narrowers_concept").append("<h2> Actors from narrowers of concept </h2>");
    $(retdata).each( function() {
        //alert(this.actors);
        var narrower = this.narrower;
        var narrower_dom = narrower.replace(/,/g,"").replace(/ /g,"");
        $(".actors_narrowers_concept").append("<h4>" + narrower + "</h4><ul id='results-" + narrower_dom + "'></ul>");
        $(this.actors).each(function(){
            $('#results-'+narrower_dom).append(
                '<li>' + this[0] + ', ' + this[1] + '</li>' );
            });
    });
};

function abc_image(retdata) {
    window.abc_image = retdata;
    $(".actors_broaders_concept_image").append("<IMG width='800px' src='"+retdata.image_url+"'/>");
};
   