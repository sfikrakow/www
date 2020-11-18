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


// Mail handling


const sendMailBtn = document.querySelector('#sendMail');

const cleanForm = () => {
  document.querySelector('#name').value = '';
  document.querySelector('#email').value = '';
  document.querySelector('#topic').value = '';
  document.querySelector('#message').value = '';
}

const showStatus = async (e) => {
  e.preventDefault();
  const URL = '/contact_form/';
  const data = new URLSearchParams(new FormData(document.querySelector("form")));
  const headers = new Headers();
  headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

  const response = await fetch(URL, {
    method: 'POST',
    body: data,
    headers: headers,
  });

  // Temporary
  if (response.status === 200) {
    cleanForm();
    console.log('Succes');
  } else {
    console.log('Error');
  }

}

sendMailBtn.addEventListener('click', (e) => showStatus(e));