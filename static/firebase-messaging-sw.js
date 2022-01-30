importScripts("https://www.gstatic.com/firebasejs/8.1.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.1.0/firebase-messaging.js");

const firebaseConfig = {
    apiKey: "AIzaSyDupVPtJAQ_2csaCwcS66XM7OkAdyk4dEw",
    authDomain: "test1211-7b1d8.firebaseapp.com",
    projectId: "test1211-7b1d8",
    storageBucket: "test1211-7b1d8.appspot.com",
    messagingSenderId: "53893167055",
    appId: "1:53893167055:web:b55dbd805ddc9e35d404ba",
    measurementId: "G-SK2Q1M1W5F"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging()
// Get registration token. Initially this makes a network call, once retrieved
// subsequent calls to getToken will return from cache.
console.log('sw js')
/*messaging.getToken({ vapidKey: 'BI4HIQl8aZnXKDrEDB8xixu_E3vfODhD38CZKntyymPuff3Sdl99WfY44FOMdbEueahnG0rOSIWYhD8yn6VHbaw' }).then((currentToken) => {
    if (currentToken) {
      // Send the token to your server and update the UI if necessary
      // ...
      console.log(currentToken)
      console.log('tut token')
      //localStorage.setItem('token', currentToken);
    } else {
      // Show permission request UI
      console.log('No registration token available. Request permission to generate one.');
      // ...
    }
  }).catch((err) => {
    console.log('An error occurred while retrieving token. ', err);
    // ...
  });*/

  messaging.setBackgroundMessageHandler(function(payload) {
    console.log(payload)
  })