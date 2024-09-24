document.addEventListener("DOMContentLoaded", () => {
  for (const el of document.querySelectorAll(".groups a.addlink")) {
    el.innerText = ""
  }

  const quickpanel = document.getElementById("quickpanel")
  const header = document.querySelector("#header h1")
  if (quickpanel && header) {
    document.body.classList.add("qp-active")
    header.addEventListener("click", (e) => {
      e.preventDefault()
      document.body.classList.toggle("qp-open")
    })
  }
})
