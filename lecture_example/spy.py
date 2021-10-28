from lecture_example.demo_for_di import ExamScoreHandler


class FakeDatabase:
    def get_all_score(self, name):
        return [100, 90, 95]


def test_get_total_score(mocker):
    fake_database = FakeDatabase()
    score_handler = ExamScoreHandler(fake_database)
    spy = mocker.spy(fake_database, 'get_all_score')
    assert score_handler.get_total_score("Andy") == 285

    spy.assert_called_with("Any")
    assert spy.call_count == 1

