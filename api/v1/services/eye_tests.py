from sqlalchemy.orm import Session
from api.core.base.services import Service
from api.v1.models.eye_tests import SnellenChartTest, ColorBlindnessTest, TumblingETest
from api.v1.models.user import User


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

eyetest_service = EyeTestService()