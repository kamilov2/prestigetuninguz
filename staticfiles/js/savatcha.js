

// delete function from savatcha

let btnForDeleteFun = document.querySelectorAll('.btnForDeleteFun')
let itemForDelete = document.querySelectorAll('.itemForDelete')
let clearAll = document.getElementById('clearAll')

btnForDeleteFun.forEach((item, index) => {
  item.addEventListener('click', () => {
    itemForDelete[index].remove()
  })
})

clearAll.addEventListener('click', () => {
  itemForDelete.forEach((item) => {
    item.remove()
  })
})