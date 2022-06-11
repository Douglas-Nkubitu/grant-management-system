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
      $(".cards-parent").removeClass("hide");
      $("#search-empty-state").addClass("hide");
      return;
    }

    frappe.call({
        method: "erpnext.non_profit.doctype.grant_call.grant_call.open_search_grant",
        args: {
            "text": input
        },
        callback: (data) => {
            render_grant_list(data.message);
        }
     });
}

const render_grant_list = (active_grant_list) => {
    $("#search-empty-state").addClass("hide");
  
    if (!active_grant_list.length) {
      $(".cards-parent").removeClass("hide");
      $("#search-empty-state").removeClass("hide");
      return;
    }
  
     $(".cards-parent").addClass("hide");
  //   for (grantcall in active_grant_list) {
  //     // $("[data-grantcall=" + active_grant_list[grantcall].name + "]").removeClass("hide");
  //     $(".cards-parent").append(grantcall);
  // }
}

const close_search_empty_state = (e) => {
    $("#search-empty-state").addClass("hide");
    $("#search-grant").val("").keyup();
}
  