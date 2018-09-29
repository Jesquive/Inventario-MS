
$(document).ready(function(){
  var navbar = document.getElementById("sidebar-active");
  if(title == "Dashboard"){
    navbar.childNodes[0].classList.add("active");
  } else if (title == "Productos") {
    navbar.childNodes[2].classList.add("active");
  }
});
