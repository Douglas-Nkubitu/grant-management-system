frappe.ready(() => {

    $(".close-search-empty-state").click((e) => {
      close_search_empty_state(e);
    });
  
    $("#search-grant").keyup(function() {
      let timer;
      clearTimeout(timer);
      timer = setTimeout(() => {search.apply(this, arguments);}, 300);
    });
  
});
 
const search = (e) => {
    let input = $(e.currentTarget).val();  
    if (input == window.input)
      return;  
    window.input = input;
  
    if (input.length < 3 || input.trim() == "") {
      $(".card-parent").removeClass("hide");
      $("#search-empty-state").addClass("hide");
      return;
    }

    frappe.call({
        method: "erpnext.non_profit.doctype.grant_call.grant_call.closed_search_grant",
        args: {
            "text": input
        },
        callback: (data) => {
            render_grant_list(data.message);
        }
     });
}

const render_grant_list = (closed_grant_list) => {
    $("#search-empty-state").addClass("hide");
  
    if (!closed_grant_list.length) {
      $(".card-parent").removeClass("hide");
      $("#search-empty-state").removeClass("hide");
      return;
    }
  
     $(".card-parent").addClass("hide");
    for (grantcall in closed_grant_list) {
      $(".cards-parent").append(grantcall);
    //  $("[data-grantcall=" + closed_grant_list[grantcall].name + "]").removeClass("hide");
    }
  }

const close_search_empty_state = (e) => {
    $("#search-empty-state").addClass("hide");
    $("#search-grant").val("").keyup();
}
  