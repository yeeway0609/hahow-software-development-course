class ExamScoreHandler:
    def __init__(self, injected_database):
        self.database = injected_database

    def get_total_score(self, name):
        # 從資料庫取的學生所有成績，假設返回一個 list
        # 使用「從外部 inject」的 Database
        score_list = self.database.get_all_score(name)
        return sum(score_list)

def test_get_total_score():
    score_handler = ExamScoreHandler(FakeDatabase())
    assert score_handler.get_total_score("Andy") == 300
