/* global django */
document.addEventListener("DOMContentLoaded", function () {
  django.jQuery(function ($) {
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
