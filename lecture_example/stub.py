from lecture_example.demo_for_di import ExamScoreHandler


class FakeDatabase:
    def get_all_score(self, name):
        return [100, 90, 95] if name == "Andy" else []


def test_get_total_score():
    fake_database = FakeDatabase()
    score_handler = ExamScoreHandler(fake_database)
    assert score_handler.get_total_score("Andy") == 285
