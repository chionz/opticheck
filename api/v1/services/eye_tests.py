from sqlalchemy.orm import Session
from sqlalchemy import cast, select, union_all, literal_column, String, desc
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
        ratio = schema.user_acuity / schema.normal_acuity
        print(ratio)

        # realistic clinical numbers
        snellen_steps = [200, 100, 80, 60, 50, 40, 30, 25, 20]

        #converting ratio to user acuity
        normal_acuity = int(round((schema.user_acuity/schema.user_acuity)*40))
        denominator_ratio = int(round(normal_acuity / ratio)) if ratio > 0 else 200

        # Find the closest standard denominator
        closest = min(snellen_steps, key=lambda x: abs(x - denominator_ratio))

        """ # Mathematical Conversions
        user_acuity = int(round((schema.user_acuity/schema.user_acuity)*40))
        normal_acuity = int(round((schema.normal_acuity/schema.user_acuity)*40)) """

        result = {"user_id": user_id,
        "eye_tested": "left",
        "normal_acuity": normal_acuity,
        "user_acuity": ratio,
        "visual_acuity": f'{normal_acuity}/{closest}',
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
        snellen_user_test = db.query(SnellenChartTest).filter(SnellenChartTest.user_id==user_id).count()

        return snellen_user_test
        
    def color_blindness_test_count(self, db:Session, user_id):
        snellen_user_test = db.query(ColorBlindnessTest).filter(ColorBlindnessTest.user_id==user_id).count()

        return snellen_user_test
    
    def tumbling_etest_count(self, db:Session, user_id):
        snellen_user_test = db.query(TumblingETest).filter(TumblingETest.user_id==user_id).count()

        return snellen_user_test
    
    def all_test_count(self, db:Session, user_id):
        colour = self.color_blindness_test_count(db, user_id)
        snellen = self.snellen_chart_count(db, user_id)
        tubling = self.tumbling_etest_count(db, user_id)

        all_count = colour + snellen + tubling

        return all_count
    
    def dashboard_vision_test(self, db:Session, user_id):
        snellen = db.query(SnellenChartTest).filter(SnellenChartTest.user_id==user_id).order_by(SnellenChartTest.tested_at.desc()).first()

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
    
        
    def user_tests(self, db: Session, user_id: str):
        snellen_q = (
            select(
                SnellenChartTest.id.label("id"),
                SnellenChartTest.user_id.label("user_id"),
                SnellenChartTest.tested_at.label("tested_at"),
                cast(SnellenChartTest.visual_acuity, String).label("result"), 
                literal_column("'snellen'").label("test_type"),
            )
            .where(SnellenChartTest.user_id == user_id)
        )

        color_q = (
            select(
                ColorBlindnessTest.id.label("id"),
                ColorBlindnessTest.user_id.label("user_id"),
                ColorBlindnessTest.tested_at.label("tested_at"),
                cast(ColorBlindnessTest.score, String).label("result"),
                literal_column("'color_blindness'").label("test_type"),
            )
            .where(ColorBlindnessTest.user_id == user_id)
        )

        tumbling_q = (
            select(
                TumblingETest.id.label("id"),
                TumblingETest.user_id.label("user_id"),
                TumblingETest.tested_at.label("tested_at"),
                cast(TumblingETest.score, String).label("result"),
                literal_column("'tumbling_e'").label("test_type"),
            )
            .where(TumblingETest.user_id == user_id)
        )

        lea_q = (
            select(
                LeaSymbolsETest.id.label("id"),
                LeaSymbolsETest.user_id.label("user_id"),
                LeaSymbolsETest.tested_at.label("tested_at"),
                cast(LeaSymbolsETest.score, String).label("result"),
                literal_column("'lea_symbols'").label("test_type"),
            )
            .where(LeaSymbolsETest.user_id == user_id)
        )

        # Combine with UNION ALL
        union_q = snellen_q.union_all(color_q, tumbling_q, lea_q).subquery()

        # Apply ORDER BY tested_at DESC
        ordered_q = select(union_q).order_by(desc(union_q.c.tested_at))

        # Run & fetch as dict-like rows
        results = db.execute(ordered_q).mappings().all()


        return [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "result": row["result"],
                "tested_at": row["tested_at"],
                "test_type": row["test_type"], 
            }
            for row in results
        ]


eyetest_service = EyeTestService()