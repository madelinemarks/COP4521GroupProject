function redirect(element) {     
    var $row = $(element).closest("tr");
    var $title = $row.find(".title").text();
    var $isbn = $row.find(".isbn").text();
    var $asking = $row.find(".asking").text();

    var form = $(document.createElement('form'));
       $(form).attr("action", "/checkout");
       $(form).attr("method", "POST");
       $(form).css("display", "none");

    var input_title = $("<input>")
       .attr("type", "text")
       .attr("name", "title")
       .val($title);
    $(form).append($(input_title));

    var input_isbn = $("<input>")
       .attr("type", "text")
       .attr("name", "isbn")
       .val($isbn);
    $(form).append($(input_isbn));

    var input_asking = $("<input>")
       .attr("type", "text")
       .attr("name", "asking")
       .val($asking);
    $(form).append($(input_asking));

    form.appendTo(document.body);
    $(form).submit();
}