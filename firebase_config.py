import pyrebase

config = {
    "apiKey": "AIzaSyCwqRy-HL1yM2R-VBVhLJ7JUxrYu-kznUs",
    "authDomain": "elephant-detection-ab063.firebaseapp.com",
    "projectId": "elephant-detection-ab063",
    "storageBucket": "elephant-detection-ab063.appspot.com",
    "messagingSenderId": "389100082853",
    "appId": "1:389100082853:web:cc90944cff290b085b5f4c",
    "measurementId": "G-R393BKFJDG"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app.run(debug=True)
