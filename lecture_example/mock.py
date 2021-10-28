from unittest.mock import Mock

from lecture_example.demo_for_di import ExamScoreHandler


def test_get_total_score():
    fake_database = Mock()
    fake_database.get_all_score = Mock(return_value=[100, 90, 95])
    score_handler = ExamScoreHandler(fake_database)

    assert score_handler.get_total_score("Andy") == 285
    fake_database.get_all_score.assert_called_with("Andy")
