// Asynchronously print some activity info
h={
 'DI-Backend':'connectapi.garmin.com',
 'Authorization':'Bearer '+JSON.parse(localStorage.token).access_token
}

jQuery.ajax({
 headers: h,
 url: 'https://connect.garmin.com/activitylist-service/activities/search/activities?activityType=running&startDate=2019-09-15&endDate=2019-12-31&limit=5&start=0&_=1577777388000',
 success: all => all.forEach(async a=>{
   await new Promise(s=>setTimeout(s,t+=2000))
   console.dir(a.activityId, a.activityName, a.startTimeLocal)
  })
})

// ----------------------------------------------------------------
// EDIT 1 piece of gear
GT2000ID = '401db7e05626493f912bb6cc53283d83'
h={
 'DI-Backend':'connectapi.garmin.com',
 'Authorization':'Bearer ' + JSON.parse(localStorage.token).access_token,
'Accept': 'application/json',
};
 jQuery.ajax({
  headers: h,
  url:'/gear-service/gear/link/'+ GT2000ID + '/activity/' + '4372877162',
  method: 'PUT',
  complete: function(xhr, textStatus) {
    console.log(xhr.status);
}
});

// EDIT ALL GEAR between dates
console.log(JSON.parse(localStorage.token).access_token)
GT2000ID = '401db7e05626493f912bb6cc53283d83'
h={
 'DI-Backend':'connectapi.garmin.com',
 'Authorization':'Bearer '+JSON.parse(localStorage.token).access_token
};
jQuery.ajax({
 headers: h,
 url: 'https://connect.garmin.com/activitylist-service/activities/search/activities?activityType=running&startDate=2019-09-15&endDate=2020-01-04&limit=50&start=0&_=1577777388000',
 success: function(act_list) {
    act_list.forEach(
        function(act){
             jQuery.ajax({
                  headers: {
                     'DI-Backend':'connectapi.garmin.com',
                     'Authorization':'Bearer ' + JSON.parse(localStorage.token).access_token,
                     'Accept': 'application/json',
                    },
                  url:'/gear-service/gear/link/'+ GT2000ID + '/activity/' + act['activityId'],
                  method: 'PUT',
                  complete: function(xhr, textStatus) {
                        console.log(act['activityId'], xhr.status);
                  } 
            });
        })
	}
});
