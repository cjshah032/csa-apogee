function getTimeRemaining(endTime){
    const total = Date.parse(endTime) - Date.parse(new Date());
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
    const days = Math.floor(total / (1000 * 60 * 60 * 24));
    
    return {
        total,
        days,
        hours,
        minutes,
        seconds
    };
}

function initializeClock(id,startTime,endTime){
    const clock=document.getElementById(id);
    if(!clock) return;
    function updateClock() {
        const t1 = getTimeRemaining(startTime);
        const t2 = getTimeRemaining(endTime);
        if(t1.total>=0){
            clock.innerHTML = ('Live in ') + ((t1.days>0)?t1.days+'D ':'') + ((t1.hours>0)?t1.hours+'H ':'')
                + ((t1.minutes>0)?t1.minutes+'M ':'') + ((t1.seconds>0)?t1.seconds+'S ':'');
            clock.style.color = 'blue';
        }
        else if(t2.total>=0){
            clock.innerHTML = ('Live Now: ') + ((t2.days>0)?t2.days+'D ':'') + ((t2.hours>0)?t2.hours+'H ':'') + ((t2.minutes>0)?t2.minutes+'M ':'') + ((t2.seconds>0)?t2.seconds+'S ':'') + 'Left';
            clock.style.color = 'green';
        }
        else {
            clock.innerHTML = 'Ended';
            clock.style.color = 'red';
            clearInterval(timeinterval);
        }
      };
      updateClock();
      var timeinterval = setInterval(updateClock,1000);
}

const qriousStart=new Date("20 Mar, 2022 00:01:00");
const qriousEnd=new Date("31 Mar, 2022 23:59:00");

const anticodingStart=new Date("20 Mar, 2022 15:30:00");
const anticodingEnd=new Date("31 Mar, 2022 16:30:00");

const datageddonStart=new Date("21 Mar, 2022 15:00:00");
const datageddonEnd=new Date("31 Mar, 2022 17:00:00");

initializeClock('qriouscountdown',qriousStart,qriousEnd);
initializeClock('anticodingcountdown',anticodingStart,anticodingEnd);
initializeClock('datageddoncountdown',datageddonStart,datageddonEnd);