
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
    this.render()
  }

  attributeChangedCallback(name, oldv, newv) {
    if (oldv !== newv && oldv) {
      console.log("old:", oldv, " new:", newv)
      this.render()
    }
  }

  render() {
    let template = this.getAttribute('page-type') + "-template"
    let templateLocation = document.getElementById(template)
    if (templateLocation) {
      this.innerHTML = templateLocation.innerHTML
    } else {
      this.innerHTML = ""
    }
  }

}

customElements.define('dashboard-page', Pages)