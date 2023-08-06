$(document).ready(function () {
    $('#table_tags thead tr th').click(function () {
        var kids = $( this ).children("i");
        if (kids.length == 0){
            // trier
            var params = new URLSearchParams(window.location.search);
            params.set("sortby", $( this ).attr('id') );
            params.set("sortbydirection", "desc");
            window.location.replace(window.location.pathname + '?' + params.toString());
        } else {
            // inversion du trie
            var params = new URLSearchParams(window.location.search);
            params.set("sortbydirection", params.get("sortbydirection") == "desc" ? "asc" : "desc");
            window.location.replace(window.location.pathname + '?' + params.toString());
        }
    })
});
