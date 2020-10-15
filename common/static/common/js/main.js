const hamburgerBtn = document.querySelector('.hamburger');
const navbarLinks = document.querySelector('.navbar__links');

// Toggle the hamburger button and the navbar links on click
hamburgerBtn.addEventListener('click', (e) => {
  hamburgerBtn.classList.toggle('is-active');
  navbarLinks.classList.toggle('is-active');
});

// Dropdown logic
const dropdowns = [...document.querySelectorAll('.dropdown__title')];

function handleDropdown() {
  this.parentNode.classList.toggle('active');
  const answer = this.nextElementSibling;
  const height = `${answer.scrollHeight}px`;
  answer.style.maxHeight = !answer.style.maxHeight ? height : null;
}

if(dropdowns) {
  dropdowns.forEach(dropdown => dropdown.addEventListener('click', handleDropdown));
}
