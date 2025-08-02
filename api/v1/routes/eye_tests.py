from fastapi import (
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
    APIRouter,
    Response,
    Request,
)

from api.db.database import get_db
from sqlalchemy.orm import Session
from api.utils.success_response import success_response
from api.v1.models.user import User
from api.v1.schemas.eye_tests import LeaSymbolTest, SnellenTest, ColorTest, TumblingTest
from api.v1.services.user import user_service
from api.v1.services.eye_tests import eyetest_service


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