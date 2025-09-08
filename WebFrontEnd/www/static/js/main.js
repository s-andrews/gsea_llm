$( document ).ready(function() {

    $("#runanalysis").click(run_analysis)
})


function run_analysis(){

    alert("Running analysis")
    // We need to collect the information from the form and then
    // submit an ajax request 

    
    let user_data = {
        "species": $("#species").val(),
        "query" : $("#query").val(),
        "background" : $("#background").val()
    }

    $.ajax(
        {
            url: "/runanalysis",
            method: "POST",
            data: user_data,
            success: function(folder) {
                window.location.replace(`./jobs/${folder}`)
            },
            error: function(message) {
                alert("Failed to run analysis: "+message)
            }
        }
    )
}