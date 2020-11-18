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

const inputName = document.querySelector('#name');
const inputEmail = document.querySelector('#email');
const inputTopic = document.querySelector('#topic');
const inputMessage = document.querySelector('#message');
const sendMailBtn = document.querySelector('#sendMail');

const showStatus = async (e) => {
  e.preventDefault();
  const URL = '/contact_form';
  const data = {
    name: inputName.value,
    email: inputEmail.value,
    topic: inputTopc.value,
    message: inputMessage.value,
  }

  const response = await fetch(URL, {
    method: 'POST',
    body: data,
  });

  // Temporary
  if (response.status === 200) {
    console.log('Succes');
  } else {
    console.log('Error');
  }

}

sendMailBtn.addEventListener('click', (e) => showStatus(e));