const $hamburgerBtn = document.querySelector('#dropdown');
const $navbarControls = document.querySelector('.navbar__controls');

// Toggle the hamburger button and the navbar controls on click
$hamburgerBtn.addEventListener('click', (e) => {
    e.currentTarget.classList.toggle('is-active');
    $navbarControls.classList.toggle('navbar__controls--show')
})