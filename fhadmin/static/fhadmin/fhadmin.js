document.addEventListener("DOMContentLoaded", function () {
  window.django && window.django.jQuery && window.django.jQuery(function ($) {
    $("head").append(
      '<style type="text/css">#header h1:hover { cursor: pointer; }\x3C/style>'
    )
    var quickpanel = $("#quickpanel")
    $("body").addClass("qp-active")
    $("#header h1").bind("click", function () {
      $("body").toggleClass("qp-open")
      quickpanel.slideToggle()
    })
  })
})
