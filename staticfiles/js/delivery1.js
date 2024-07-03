const goods__burger = document.getElementById("goods_burger");
const goods__close = document.getElementById("goods__close");
const goods__nav = document.getElementById("goods__nav");

goods__burger.addEventListener("click", () => {
  goods__nav.classList.add("left-0");
  goods__nav.classList.remove("left-full");
});
goods__close.addEventListener("click", () => {
  goods__nav.classList.remove("left-0");
  goods__nav.classList.add("left-full");
});

const catalog = document.getElementById("catalog");
const catalogDiv = document.getElementById("catalogDiv")

catalog.addEventListener("click", () => {
    if(document.body.style.overflow != "hidden"){
        document.body.style.overflow = 'hidden'

    }else{
        document.body.style.overflow = 'auto'
    }
    catalog.classList.toggle('bg-black')
    catalogDiv.classList.toggle('md:top-[180px]')
    catalogDiv.classList.toggle('top-[150px]')
    catalogDiv.classList.toggle('top-[100%]')
    catalogDiv.classList.toggle('md:top-[100%]')

})
