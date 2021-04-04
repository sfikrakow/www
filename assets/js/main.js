const hamburgerBtn = document.querySelector('.hamburger');
const navbarLinks = document.querySelector('.navbar__links');

// Toggle the hamburger button and the navbar links on click
hamburgerBtn.addEventListener('click', (e) => {
  hamburgerBtn.classList.toggle('is-active');
  navbarLinks.classList.toggle('is-active');
});


// Mail handling
const contactForm = document.querySelector('#contact-form');

function handleResultMessage(hasSucceeded) {
  document.querySelectorAll('.form-result').forEach(p => p.style.display = 'none');

  if (hasSucceeded) {
    document.querySelector('.footer-contact__form-positive').style.display = 'block';
  } else {
    document.querySelector('.footer-contact__form-negative').style.display = 'block';
  }
}

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

  if (response.status === 200) {
    contactForm.reset();
    handleResultMessage(true);
  } else {
    handleResultMessage(false);
  }
}

global.doCaptcha = function() {
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
document.getElementById('contact-form-button').type = 'submit';


const agendaHandler = (event) => {
  agendaButtons.forEach((agendaButton) => {
    agendaButton.classList.remove('active');
  });

  event.target.classList.add('active');
  agendaDays.forEach((agendaDay) => {
    agendaDay.style.opacity = 0;
  });

  const index = Number(event.target.dataset.index);
  agendaDays[index].style.opacity = 1;
}
const agendaButtons = document.querySelectorAll('.agenda__navigation-day');
const agendaDays = document.querySelectorAll('.agenda__day');

// Make 1st day visible by default
agendaButtons[0].classList.add('active');
agendaDays[0].style.opacity = 1;

agendaButtons.forEach((agendaButton) => agendaButton.addEventListener('click', agendaHandler));
