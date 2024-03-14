function setIndex() {
  let pages = document.querySelectorAll(".page");
  for (var i = 0; i < pages.length; i++) {
    pages[i].style.zIndex = pages.length - i;
  }
}

setIndex();

function previous() {
  let active = document.querySelector(".active");
  let prevSib = active.previousElementSibling;
  active.className = "page";
  prevSib.className = "page active";
  setIndex();
  prevSib.style.transform = "rotateY(0deg)";
  let prevSib2 = prevSib.previousElementSibling;
  if (prevSib2 && prevSib2.className == "page") {
    prevSib2.style.zIndex = "9998";
  }
}

function next() {
  let active = document.querySelector(".active");
  let nextSib = active.nextElementSibling;
  active.style.transform = "rotateY(180deg)";
  active.className = "page";
  setIndex();
  active.style.zIndex = "9998";
  if (nextSib) {
    nextSib.className = "page active";
  }
}