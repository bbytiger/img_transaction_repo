
const change_page = function(event) {
  let extract = String(event.target.innerHTML).toLowerCase()
  let splitString = extract.split(" ")
  let resString = splitString.join("-")
  document.getElementById('dashboard-page-switch').setAttribute('page-type', resString)
  document.getElementById('dashboard-page-switch').getAttribute('page-type')
}

class Pages extends HTMLElement {
  static get observedAttributes() {
    return ['page-type']
  }

  constructor() {
    super()
    this.innerHTML = ""
  }

  connectedCallback() {
    this.render(false)
  }

  attributeChangedCallback(name, oldv, newv) {
    if (oldv !== newv && oldv) {
      console.log("old:", oldv, " new:", newv)
      this.render(true)
    }
  }

  render(change_needed) {
    let template = this.getAttribute('page-type') + "-template"
    let templateLocation = document.getElementById(template)
    if (templateLocation) {
      console.log(this)
      let child = document.querySelector('#dashboard-page-switch').querySelector('#child')
      console.log(child)
      if (change_needed && child) {
        this.removeChild(child);
      }
      console.log(templateLocation)
      this.appendChild(templateLocation.content)
    }
  }

}

customElements.define('dashboard-page', Pages)