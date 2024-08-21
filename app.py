from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin 
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong key

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\User\OneDrive\Desktop\FYP webapp\elephant-detection-ab063-firebase-adminsdk-mwxh7-24d36a15e4.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    try:
        # Fetch user by email
        user = auth.get_user_by_email(email)
        session['user'] = user.uid
        
        # Fetch elephant detection data
        detection_data = db.collection('elephant_detections').stream()
        detected_data_list = [doc.to_dict() for doc in detection_data]

        return render_template('dashboard.html', detection_data=detected_data_list)
    except firebase_admin._auth_utils.UserNotFoundError:
        return render_template('login.html', error="User not found.")
    except Exception as e:
        print(f"Error during login: {e}")
        return render_template('login.html', error="Incorrect email or password.")


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        # Fetch elephant detection data from Firestore
        detections_ref = db.collection('elephant_detections')
        docs = detections_ref.stream()
        detected_data = [doc.to_dict() for doc in docs]
        
        return render_template('dashboard.html', data=detected_data)
    return redirect(url_for('index'))


        
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    contact = request.form['contact']
    email = request.form['email']
    password = request.form['password']
    
    try:
        # Create a new user with email and password
        user = auth.create_user(email=email, password=password)
        
        # Save additional user data in Firestore
        user_uid = user.uid  # Firebase user ID
        user_data = {
            'name': name,
            'contact': contact,
            'email': email
        }
        db.collection("users").document(user_uid).set(user_data)
        
        return redirect(url_for('index'))
    except Exception as e:
        return f"Registration Failed: {str(e)}"



@app.route('/settings')
def settings():
    if 'user' in session:
        return render_template('settings.html')
    return redirect(url_for('index'))

@app.route('/manage_devices')
def manage_devices():
    if 'user' in session:
        return render_template('manage_devices.html')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
