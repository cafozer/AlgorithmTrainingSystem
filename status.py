class Status:
    def __init__(self, problem_id, user_id, solved = -1):
        self.problem_id = problem_id
        self.user_id = user_id
        self.solved = solved