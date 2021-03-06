import os
import pathlib
import pyrebase
import firebase_admin
from datetime import date
from dotenv import load_dotenv, dotenv_values
from firebase_admin import auth, credentials, firestore


BASE_DIR = pathlib.Path(__file__).parent.absolute()
CRED_DIR = BASE_DIR / 'firebase-sdk.json'

load_dotenv(dotenv_path = BASE_DIR / '.env')

config = {
  "apiKey": os.getenv('PYREBASE_API_KEY'),
  "authDomain": "master-yoga-ef07c.firebaseapp.com",
  "databaseURL": "https://master-yoga-ef07c-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "master-yoga-ef07c",
  "storageBucket": "master-yoga-ef07c.appspot.com",
  "messagingSenderId": "406827781078",
  "appId": "1:406827781078:web:ae92f6607c4e74abccf277",
  "measurementId": "G-BQ1B138K0D"
}

cred = credentials.Certificate(CRED_DIR)
firebase_admin.initialize_app(cred)
db = firestore.client()


# ************************************************
# *******************   AUTH   *******************
# ************************************************

pyrebase = pyrebase.initialize_app(config)
pyrebaseAuth = pyrebase.auth()

def logIn(email, password):
  try:
    loginResult = pyrebaseAuth.sign_in_with_email_and_password(email, password)
    return {
      'success': True,
      'msg': 'User has been logged in',
      'result': loginResult
    }
  except Exception as e:
    print(e)
    return {
      'success':False,
      'msg': str(e)
    }

def authToken(token):
  try:
    decoded_token = auth.verify_id_token(token)
    return {
      'valid': True,
      'msg':'Token verified',
      'result': decoded_token
    }
  except Exception as e:
    print(e)
    return {
      'valid': False,
      'msg':'Token is invalid',
      'result':'null'
    }

def getUser(uid):
  user = db.collection('users').document(uid).get()
  processedUser = user
  if processedUser:
    return processedUser.to_dict()
  else:
    return False

def registerUser(userData):
  try:
    user = auth.create_user(
      email=userData['email'],
      email_verified=False,
      password=userData['password'],
      display_name='{userData[firstName]} {userData[lastName]}',
      disabled=False
    )
    uid = user.uid
    registerUserData = {
      'firstName': userData['firstName'],
      'lastName': userData['lastName'],
      'consecutiveDays': 0,
      'customTracks': [],
      'email': userData['email'],
      'image':'url',
      'lastEntry': str(date.today()),
      'posesCompletion': []
    }
    poses = getPosesList()
    if poses:
      registerUserData['posesCompletion'] = poses
    db.collection('users').document(uid).set(registerUserData)
    newUser = db.collection('users').document(uid).get()
    return {
      'success': True,
      'password': userData['password'],
      'userData': newUser.to_dict()
    }
  except Exception as e:
    print(e)
    return {
      'success': False,
      'msg': e
    }

def updateUser(uid, userData):
  db.collection('users').document(uid).update(userData)
  return db.collection('users').document(uid).get().to_dict()

# ************************************************
# ******************* DATABASE *******************
# ************************************************

def newUser(data):
  uid = data['user_id']
  name = data['name'].split()
  userData = {
    'firstName': name[0],
    'lastName': name[1],
    'email': data['firebase']['identities']['email'][0],
    'consecutiveDays': 0,
    'customTracks': [],
    'image':data['picture'],
    'lastEntry': str(date.today()),
    'posesCompletion': []
  }
  try:
    poses = getPosesList()
    if poses:
      userData['posesCompletion'] = poses
    db.collection('users').document(uid).set(userData)
    newUser = db.collection('users').document(uid).get()
    return newUser.to_dict()
  except:
    print('Failed to create new user in database')
    raise


def getPoses():
  try:
    posesCollection = db.collection('poses').get()
    posesList = []
    for pose in posesCollection:
      posesList.append(pose.to_dict())
    return posesList
  except:
    print('Failed to retrieve poses from database')
    raise

def getRoutines():
  try:
    routinesCollection = db.collection('routines')
    result = {}
    for routineSnapshot in routinesCollection.get():
      name = routineSnapshot.id
      formattedRoutines = []
      for pose in routineSnapshot.to_dict()['routineList']:
        formattedRoutines.append(pose)
      result[name] = formattedRoutines
      result[name + '_description'] = routineSnapshot.to_dict()['level_description']
    return result
  except:
    print('Failed to retrieve routines from database')
    raise

# ************************************************
# ******************* HELPERS  *******************
# ************************************************

def getPosesList():
  try:
    poses = db.collection('poses').get()
    posesList = []
    for pose in poses:
      tempPose = pose.to_dict()
      posesList.append({'id': tempPose['id'], 'level': tempPose['level'], 'percentage': 0})
    return posesList
  except:
    print('Failed to retrieve routines from database')
    raise