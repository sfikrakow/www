const $hamburgerBtn = document.querySelector('#dropdown');
const $navbarLinks = document.querySelector('.navbar__links');

// Toggle the hamburger button and the navbar links on click
$hamburgerBtn.addEventListener('click', (e) => {
  $hamburgerBtn.classList.toggle('is-active');
  $navbarLinks.classList.toggle('navbar__links--show');
});