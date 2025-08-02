from sqlalchemy.orm import Session
from api.core.base.services import Service
from api.v1.models.eye_tests import LeaSymbolsETest, SnellenChartTest, ColorBlindnessTest, TumblingETest
from api.v1.models.user import User
from api.v1.schemas.eye_tests import ColorTest, LeaSymbolTest, SnellenTest, TumblingTest


class EyeTestService(Service):
    def create(self):
        pass

    def fetch(self):
        pass

    def fetch_all(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def snellen_test_create(self, db:Session, schema:SnellenTest, user_id:str):
        result = {"user_id": user_id,
        "eye_tested": "left",
        "normal_acuity": schema.normal_acuity,
        "user_acuity": schema.user_acuity,
        "visual_acuity": f'{schema.user_acuity}/{schema.normal_acuity}',
        "distance": schema.distance}

        test = SnellenChartTest(**result)
        db.add(test)
        db.commit()
        db.refresh(test)

        return test

    def user_snellen_tests(self, db:Session, user_id):

        tests = db.query(SnellenChartTest).filter(user_id==user_id).all()

        return tests
    
    def delete_user_snellen_tests(self, db:Session, user_id, test_id):

        tests = db.query(SnellenChartTest).filter(SnellenChartTest.user_id==user_id, SnellenChartTest.id==test_id).first()

        db.delete(tests)
        db.commit()
        db.refresh(tests)

        return tests

    def snellen_chart_count(self, db:Session, user_id):
        snellen_user_test = db.query(SnellenChartTest).filter(user_id==user_id).count()

        return snellen_user_test
        
    def color_blindness_test_count(self, db:Session, user_id):
        snellen_user_test = db.query(ColorBlindnessTest).filter(user_id==user_id).count()

        return snellen_user_test
    
    def tumbling_etest_count(self, db:Session, user_id):
        snellen_user_test = db.query(TumblingETest).filter(user_id==user_id).count()

        return snellen_user_test
    
    def all_test_count(self, db:Session, user_id):
        colour = self.color_blindness_test_count(db, user_id)
        snellen = self.snellen_chart_count(db, user_id)
        tubling = self.tumbling_etest_count(db, user_id)

        all_count = colour + snellen + tubling

        return all_count
    
    def dashboard_vision_test(self, db:Session, user_id):
        snellen = db.query(SnellenChartTest).filter(user_id==user_id).first()

        return snellen
    

    # Color Blindness

    def color_test_create(self, db:Session, schema:ColorTest, user_id:str):
            
            result = {"user_id": user_id,
            "total_questions": schema.total_questions,
            "correct_answers": schema.correct_answers,
            "score": schema.score,}

            test = ColorBlindnessTest(**result)
            db.add(test)
            db.commit()
            db.refresh(test)

            return test
    
    def user_color_tests(self, db:Session, user_id):

        tests = db.query(ColorBlindnessTest).filter(user_id==user_id).all()

        return tests

    # Tumbling E Test
    def tumbling_test_create(self, db:Session, schema:TumblingTest, user_id:str):
            
            if schema.total_questions == 0:
                user_score = 0
            else:
                user_score = (schema.correct_answers / schema.total_questions) * 100
                
            result = {"user_id": user_id,
            "total_questions": schema.total_questions,
            "correct_answers": schema.correct_answers,
            "score": f"{user_score}%",}

            test = TumblingETest(**result)
            db.add(test)
            db.commit()
            db.refresh(test)

            return test
    
    def user_tumbling_tests(self, db:Session, user_id):

        tests = db.query(TumblingETest).filter(user_id==user_id).all()

        return tests
    
    # Lea Symbol Test
    def lea_test_create(self, db:Session, schema:LeaSymbolTest, user_id:str):
            
            if schema.total_questions == 0:
                user_score = 0
            else:
                user_score = (schema.correct_answers / schema.total_questions) * 100

            result = {"user_id": user_id,
            "total_questions": schema.total_questions,
            "correct_answers": schema.correct_answers,
            "score": f"{user_score}%",}

            test = LeaSymbolsETest(**result)
            db.add(test)
            db.commit()
            db.refresh(test)

            return test
    
    def user_lea_tests(self, db:Session, user_id):

        tests = db.query(LeaSymbolsETest).filter(user_id==user_id).all()

        return tests

eyetest_service = EyeTestService()