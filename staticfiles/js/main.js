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

let tags = document.getElementsByClassName('project-tag')
for (let i =0; tags.length > i; i++){
    tags[i].addEventListener('click',(e)=>{
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project

        fetch('http://localhost:8000/api/remove-tag/',{
            method: 'DELETE',
            headers:{
                'Content-Type':'application/json',
            },
            body:JSON.stringify({'project':projectId,'tag':tagId})
        })
        .then(response => response.json())
        .then(data => {
            e.target.remove()
        })
    })

}