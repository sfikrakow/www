const hamburgerBtn = document.querySelector('.hamburger');
const navbarLinks = document.querySelector('.navbar__links');

// Toggle the hamburger button and the navbar links on click
hamburgerBtn.addEventListener('click', (e) => {
  hamburgerBtn.classList.toggle('is-active');
  navbarLinks.classList.toggle('is-active');
});

//
//
// MAIL
//
//

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

//
//
//  AGENDA
//
//

const agendaHandler = (event) => {
  agendaButtons.forEach((agendaButton) => {
    agendaButton.classList.remove('active');
  });

  event.target.classList.add('active');
  agendaDays.forEach((agendaDay) => {
    agendaDay.style.display = 'none';
  });

  const index = Number(event.target.dataset.index);
  agendaDays[index].style.display = 'block';
}
const agendaButtons = document.querySelectorAll('.agenda__navigation-day');
const agendaDays = document.querySelectorAll('.agenda__day');

// Make 1st day visible by default
agendaButtons[0].classList.add('active');
agendaDays[0].style.display = 'block';

agendaButtons.forEach((agendaButton) => agendaButton.addEventListener('click', agendaHandler));


// The purpose of this code is to make the events that are the only ones at a given time
// take 100% of their container. Rest should take % that is in proportion to the quantity of events
// at a given time. I had to filter childNodes to remove everything that is not the div.agenda__column so I can count
// only columns and not whitespaces in the code which are text nodes in childNodes array.
document.querySelectorAll('.agenda__row').forEach((row, index) => {
  const columns = [...row.childNodes].filter((child) => child.classList?.contains('agenda__column'));

  columns.forEach((column) => {
    column.style.width = `${100 / columns.length}%`;
  });
})
