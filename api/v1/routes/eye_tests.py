from fastapi import (
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
    APIRouter,
    Response,
    Request,
    File, 
    UploadFile, 
    Form
)

import io
import speech_recognition as sr
from difflib import SequenceMatcher

from api.db.database import get_db
from sqlalchemy.orm import Session
from api.utils.success_response import success_response
from api.v1.models.user import User
from api.v1.schemas.eye_tests import LeaSymbolTest, SnellenTest, ColorTest, TumblingTest
from api.v1.schemas.token import refreshToken
from api.v1.services.user import user_service
from api.v1.services.eye_tests import eyetest_service
from api.v1.services.ai import ai_service


eye_routes = APIRouter(prefix="/test", tags=["Eye Tests"])

@eye_routes.post('/snellen-test', status_code=200, response_model=success_response)
async def snellen_chart(schema: SnellenTest,
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(user_service.get_current_user)):
    '''This Saves  User Snellen test result'''

    # Store test current user
    test = eyetest_service.snellen_test_create(db, schema=schema, user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully taken and recorded',
        data= test
    )

@eye_routes.get('/snellen-test', status_code=200, response_model=success_response)
async def user_snellen_tests_admin(user_id:str,
                            db: Session = Depends(get_db),
                            current_user: User = Depends(user_service.get_current_super_admin)):
    
    """This gets all tests done by a user (ADMIN FUNCTION)"""

    tests = eyetest_service.user_snellen_tests(db, user_id=user_id)

    return success_response(
        status_code=200,
        message='Test successfully retrieved',
        data= tests
    )
    
@eye_routes.get('/snellen-test', status_code=200, response_model=success_response)
async def user_snellen_tests(db: Session = Depends(get_db),
                             current_user: User = Depends(user_service.get_current_user)):
    
    """This gets all tests done by a user"""

    tests = eyetest_service.user_snellen_tests(db,user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully retrieved',
        data= tests
    )

@eye_routes.delete('/snellen-test', status_code=200, response_model=success_response)
async def delete_user_snellen_tests(test_id:str,
                                db: Session = Depends(get_db),
                                current_user: User = Depends(user_service.get_current_user)):
    
    """This gets all tests done by a user"""

    tests = eyetest_service.delete_user_snellen_tests(db, user_id=current_user.id, test_id=test_id)

    return success_response(
        status_code=200,
        message='Test successfully deleted',
        data= tests
    )


# This line is the beginining of ColourBlindness

@eye_routes.post('/color-test', status_code=200, response_model=success_response)
async def create_color_test(schema: ColorTest,
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(user_service.get_current_user)):
    '''This Saves  User Snellen test result'''

    # Store test current user
    test = eyetest_service.color_test_create(db, schema=schema, user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully taken and recorded',
        data= test
    )

@eye_routes.get('/color-test', status_code=200, response_model=success_response)
async def color_test(db: Session = Depends(get_db), 
                    current_user: User = Depends(user_service.get_current_user)):
    '''This gets  User color test result'''

    # get test current user
    tests = eyetest_service.user_color_tests(db,user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully retrieved',
        data= tests
    )


# This Session is the beginining of ColourBlindness
@eye_routes.post('/tumbling-e-test', status_code=200, response_model=success_response)
async def create_tumbling_test(schema: TumblingTest,
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(user_service.get_current_user)):
    '''This Saves  User Snellen test result'''

    # Store test current user
    test = eyetest_service.tumbling_test_create(db, schema=schema, user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully taken and recorded',
        data= test
    )

@eye_routes.get('/tumbling-e-test', status_code=200, response_model=success_response)
async def get_tumbling_test(db: Session = Depends(get_db), 
                    current_user: User = Depends(user_service.get_current_user)):
    '''This gets  User Tumbling test result'''

    # get test current user
    tests = eyetest_service.user_tumbling_tests(db,user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully retrieved',
        data= tests
    )

# This Session is the beginining of ColourBlindness
@eye_routes.post('/lea-symbol-test', status_code=200, response_model=success_response)
async def create_lea_test(schema: LeaSymbolTest,
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(user_service.get_current_user)):
    '''This Saves  User Snellen test result'''

    # Store test current user
    test = eyetest_service.lea_test_create(db, schema=schema, user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully taken and recorded',
        data= test
    )

@eye_routes.get('/lea-symbol-test', status_code=200, response_model=success_response)
async def get_lea_test(db: Session = Depends(get_db), 
                    current_user: User = Depends(user_service.get_current_user)):
    '''This gets  User Tumbling test result'''

    # get test current user
    tests = eyetest_service.user_lea_tests(db,user_id=current_user.id)

    return success_response(
        status_code=200,
        message='Test successfully retrieved',
        data= tests
    )

@eye_routes.post('/my-tests', status_code=200, response_model=success_response)
async def get_user_test(refresh_token:refreshToken, 
                        db: Session = Depends(get_db), ):
    print("Refresh Token Here:", refresh_token)
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="no refresh token provided")
    
    token_data = user_service.verify_refresh_token(refresh_token=refresh_token.refresh_token)
    user_id =token_data.id
    
    tests = eyetest_service.user_tests(db, user_id)

    return success_response(
        status_code=200,
        message='Test successfully retrieved',
        data= tests
    )

def similarity(a: str, b: str):
    return SequenceMatcher(None, a.upper(), b.upper()).ratio()

def letter_accuracy(expected, spoken, db, user_id):
    expected_letters = expected.replace(" ", "").upper()
    spoken_letters = spoken.replace(" ", "").upper()

    
    total = len(expected_letters)
    correct = sum(1 for a, b in zip(expected_letters, spoken_letters) if a == b)
    snellen_record = SnellenTest(
            normal_acuity=total,
            user_acuity=correct,
            distance=40,
            user_id=user_id
        )
    print(f"Expected: {expected_letters}, Spoken: {spoken_letters}, Correct: {correct}, Total: {total}, Result: {correct / total if total > 0 else 0}")

    test = eyetest_service.snellen_test_create(db, schema=snellen_record, user_id=user_id)
    ai_response = ai_service.ai_response(test.visual_acuity)

    return test, ai_response
    
    #return round(correct / total * 100, 2)


@eye_routes.post("/analyze-snellen/")
async def analyze_snellen(
    expected_text: str = Form(...),  # e.g., "E F P T O Z"
    audio_file: UploadFile = File(...),
    #user_id: str=Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_user),
):
    # Read the audio bytes
    audio_bytes = await audio_file.read()
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
    
    try:
        # Convert speech to text (using Google API built into speech_recognition)
        result = recognizer.recognize_google(audio_data)
        score = round(similarity(result, expected_text) * 100, 2)

        test, ai_response = letter_accuracy(expected_text, result, db, current_user.id)

        return success_response(
        status_code=200,
        message='Test successfully taken and recorded',
        data= {"test": test,
                "raw_result": {
                    "expected_text": expected_text,
                    "recognized_text": result,
                    "accuracy_score": score,
                    "feedback": "Good job!" if score > 80 else "Something's off"
                },
                "ai_response": ai_response
        }
    )
        
        
    except sr.UnknownValueError:
        return {"error": "Could not understand audio"}
    except sr.RequestError as e:
        return {"error": f"Speech recognition failed: {e}"}
