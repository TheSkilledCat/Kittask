//Create references to the dropdown's
const yearSelect = document.getElementById("year");
const monthSelect = document.getElementById("month");
const daySelect = document.getElementById("day");
const currentDate = new Date()



function populateYears(){
    let year = currentDate.getFullYear();
    for(let i = 0; i < 21; i++){
        const option = document.createElement("option");
        option.textContent = year + i;
        option.value = year + i
        yearSelect.appendChild(option);
    }
}

const months = ['January', 'February', 'March', 'April', 
'May', 'June', 'July', 'August', 'September', 'October',
'November', 'December'];


(function populateMonths(){
    if (yearSelect.value != currentDate.getFullYear()) {
        for(let i = 0; i < months.length; i++){
            const option = document.createElement('option');
            option.textContent = months[i];
            monthSelect.appendChild(option);
        }
    } else {
        for(let i = currentDate.getMonth(); i < months.length; i++){
            const option = document.createElement('option');
            option.textContent = months[i];
            monthSelect.appendChild(option);
        }
    }
    let currentMonth = currentDate.getMonth();
    monthSelect.value = months[currentMonth];
})();

let previousDay;

function populateDays(month){
    while(daySelect.firstChild){
        daySelect.removeChild(daySelect.firstChild);
    }
    let dayNum;
    let year = yearSelect.value;

    if(month === 'January' || month === 'March' || 
    month === 'May' || month === 'July' || month === 'August' 
    || month === 'October' || month === 'December') {
        dayNum = 31;
    } else if(month === 'April' || month === 'June' 
    || month === 'September' || month === 'November') {
        dayNum = 30;
    }else{
        if(new Date(year, 1, 29).getMonth() === 1){
            dayNum = 29;
        }else{
            dayNum = 28;
        }
    }
    for(let i = 1; i <= dayNum; i++){
        const option = document.createElement("option");
        option.textContent = i;
        daySelect.appendChild(option);
    }
    if(previousDay){
        daySelect.value = previousDay;
        if(daySelect.value === ""){
            daySelect.value = previousDay - 1;
        }
        if(daySelect.value === ""){
            daySelect.value = previousDay - 2;
        }
        if(daySelect.value === ""){
            daySelect.value = previousDay - 3;
        }
    }
}


populateDays(monthSelect.value);
populateYears();

yearSelect.onchange = function() {
    populateMonths()
    populateDays(monthSelect.value);
}
monthSelect.onchange = function() {
    populateDays(monthSelect.value);
}
daySelect.onchange = function() {
    previousDay = daySelect.value;
}

function toggleDateTime(radio) {
    var dateSelect = document.querySelector('.date-select');
    var timeSelect = document.querySelector('.time-select');
    
    if (radio.checked) {
      dateSelect.classList.add('enabled');
      timeSelect.classList.add('enabled');
      dateSelect.querySelectorAll('select').forEach(function(select) {
        select.disabled = false;
      });
      document.getElementById('time').disabled = false;
    } else {
      dateSelect.classList.remove('enabled');
      timeSelect.classList.remove('enabled');
      dateSelect.querySelectorAll('select').forEach(function(select) {
        select.disabled = true;
      });
      document.getElementById('time').disabled = true;
    }
  }

function resetDateTime() {
    var dateSelect = document.querySelector('.date-select');
    var timeSelect = document.querySelector('.time-select');
    
    dateSelect.classList.remove('enabled');
    timeSelect.classList.remove('enabled');
    dateSelect.querySelectorAll('select').forEach(function(select) {
      select.disabled = true;
    });
    document.getElementById('time').disabled = true;
  }

