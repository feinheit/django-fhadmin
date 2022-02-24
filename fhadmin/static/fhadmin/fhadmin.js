document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".groups a.addlink")
    .forEach((el) => (el.innerHTML = "&nbsp;"))

  const quickpanel = document.getElementById("quickpanel")
  const header = document.querySelector("#header h1")
  if (quickpanel && header) {
    document.body.classList.add("qp-active")
    header.addEventListener("click", () => {
      document.body.classList.toggle("qp-open")
    })
  }
})
