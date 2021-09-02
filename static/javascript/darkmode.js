let darkMode = localStorage.getItem('darkMode');
const enableDarkMode = () =>{
    document.body.classList.add('darkmode');
    document.getElementById("moon").style.display = "none";
    document.getElementById("sun").style.display = "inline";
    localStorage.setItem('darkMode','enabled');
}

const disableDarkMode = () => {
    document.body.classList.remove('darkmode')
    document.getElementById("moon").style.display = "inline";
    document.getElementById("sun").style.display = "none";
    localStorage.setItem('darkMode', null);
}
if (darkMode === 'enabled'){
    document.getElementById("moon").style.display = "inline";
    document.getElementById("sun").style.display = "none";
    enableDarkMode();
} else {
    document.getElementById("moon").style.display = "inline";
    document.getElementById("sun").style.display = "none";
};
document.getElementById('chk').onclick = function(){
    darkMode = localStorage.getItem('darkMode');
     if (darkMode != 'enabled'){
         enableDarkMode();
     }
     else{
         disableDarkMode();
     }
  };