document.addEventListener("DOMContentLoaded", () => {
  for (const el of document.querySelectorAll(".groups a.addlink")) {
    el.innerHTML = "&nbsp;"
  }

  const quickpanel = document.getElementById("quickpanel")
  const header = document.querySelector("#header h1")
  if (quickpanel && header) {
    document.body.classList.add("qp-active")
    header.setAttribute("role", "button")
    header.setAttribute("tabindex", "0")
    header.setAttribute("aria-controls", "quickpanel")
    header.setAttribute("aria-expanded", "false")

    const toggle = (e) => {
      e.preventDefault()
      const open = document.body.classList.toggle("qp-open")
      header.setAttribute("aria-expanded", open ? "true" : "false")
    }
    // The triangle is drawn on #branding::after, so listen on #branding.
    header.parentElement.addEventListener("click", toggle)
    header.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") toggle(e)
    })
  }
})
