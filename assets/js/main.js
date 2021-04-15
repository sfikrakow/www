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

agendaButtons.forEach((agendaButton) => agendaButton.addEventListener('click', agendaHandler));

const isToday = (date) => {
  const today = new Date();
  return date.getDate() === today.getDate() &&
         date.getMonth() === today.getMonth() &&
         date.getFullYear() === today.getFullYear();
}

let shouldDisplayDefaultDay = true;

agendaDays.forEach((day, index) => {
  const dayDate = new Date(day.dataset.date);
  if (isToday(dayDate)) {
    shouldDisplayDefaultDay = false;
    day.style.display = 'block';
    agendaButtons[index].classList.add('active');
  }
});

if (shouldDisplayDefaultDay && agendaDays.length > 0) {
  agendaButtons[0].classList.add('active');
  agendaDays[0].style.display = 'block';
}

//
//
// GLIDE
//
//

import Glide from '@glidejs/glide';

let slides = [...document.querySelectorAll('.glide__slide')];
const slidesContainer = document.querySelector('.glide__slides');

while (slidesContainer.firstChild) {
  slidesContainer.removeChild(slidesContainer.firstChild);
}

// Fisher-Yates Shuffle
const shuffle = (arr) => {
  let counter = arr.length;

    // While there are elements in the array
    while (counter > 0) {
      // Pick a random index
      let index = Math.floor(Math.random() * counter);

      // Decrease counter by 1
      counter--;

      // And swap the last element with it
      let temp = arr[counter];
      arr[counter] = arr[index];
      arr[index] = temp;
    }

  return arr;
}

if (slides.length) {
  shuffle(slides).forEach((slide) => {
    slidesContainer.appendChild(slide);
  });

  new Glide('.slider', {
    type: 'carousel',
    perView: 10,
    autoplay: 1000,
    animationDuration: 500,
    gap: 30,
    swipeThreshold: 0,
    dragThreshold: 0,
    breakpoints: {
      1920: {
        perView: 8
      },
      1440: {
        perView: 7
      },
      1200: {
        perView: 6,
      },
      500: {
        perView: 3
      },
    }
  }).mount();
}
