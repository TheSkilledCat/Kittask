const creationSuccess = document.getElementById('creation-success');
if (creationSuccess) {
    setTimeout(() => {
      creationSuccess.style.display = 'none';
      creationSuccess.classList.add('hide');
    }, 5000);
}

const error = document.getElementById('error');
if (error) {
    setTimeout(() => {
      error.style.display = 'none';
      error.classList.add('hide');
    }, 5000);
  }