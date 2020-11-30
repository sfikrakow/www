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

if (dropdowns) {
  dropdowns.forEach(dropdown => dropdown.addEventListener('click', handleDropdown));
}


// Mail handling


const contactForm = document.querySelector('#contact-form');

global.captchaSubmit = async function (token) {
  const URL = '/contact_form/';
  const data = new URLSearchParams(new FormData(contactForm));
  const headers = new Headers();
  headers.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

  const response = await fetch(URL, {
    method: 'POST',
    body: data,
    headers: headers,
  });

  // Temporary
  if (response.status === 200) {
    contactForm.reset();
    console.log('Succes');
  } else {
    console.log('Error');
  }

}

global.doCaptcha = function () {
  grecaptcha.reset();
  grecaptcha.execute();
}

function submitContactForm(e) {
  e.preventDefault();

  if (window.captcha !== undefined) {
    doCaptcha();
    return;
  }
  window.captcha = true;

  const script = document.createElement('script');
  document.body.appendChild(script);
  script.src = 'https://www.google.com/recaptcha/api.js?onload=doCaptcha';
}

contactForm.addEventListener('submit', submitContactForm);
