let searchForm = document.getElementById('searchForm')
let pagelink = document.getElementsByClassName('page-link')

if(searchForm){
  for(let i=0;pagelink.length>i;i++){
    pagelink[i].addEventListener('click' ,function (e){
      e.preventDefault()
      let page = this.dataset.page
      searchForm.innerHTML += `<input value=${page} name="page">`
      searchForm.submit()
    })
  }
}