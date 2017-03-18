map = {0 : '', 1 : 'block'}
function toggle(which, state) {
    document.getElementById(which).style.display = map[state]
};
function drop() {
    document.querySelector('.dropdown > ul').style.display = 'block';
}
window.onclick = function (event) {
    if (!event.target.matches('.dropdown > button')) {
        document.querySelector('.dropdown > ul').style.display = 'none';
    }
}
