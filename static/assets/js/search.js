const anasayfaMainLeft   = document.querySelector(".anasayfa-main-left");
const hamburger          = document.querySelector(".hamburger");
const searchIcon         = document.querySelector(".anasayfa-header-search-icon");
const searchArea         = document.querySelector(".anasayfa-header-search");

searchIcon.addEventListener("click", () =>{
    searchIcon.style.display = "none";
});

hamburger.addEventListener("click", () =>{
    anasayfaMainLeft.classList.toggle("show");
});

const anasayfaMainRight = document.querySelector(".anasayfa-main-right");
const angleLeft         = document.querySelector(".angle-left");
const angleRight        = document.querySelector(".angle-right");

angleLeft.addEventListener("click", () =>{
    anasayfaMainRight.classList.toggle("show");
    angleLeft.style.display = "none";
    angleRight.style.display = "block";
});

angleRight.addEventListener("click", () =>{
    anasayfaMainRight.classList.toggle("show");
    angleLeft.style.display = "block";
    angleRight.style.display = "none";
});

$('#picker').datetimepicker({
    timepicker: false,
    datepicker: true,
    format: 'y-m-d',
    value: '2021-7-2',
    inline: true,
    disabledWeekDays: [5, 6]
});