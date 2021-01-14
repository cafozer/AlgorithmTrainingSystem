from problem import Problem

class Database:
    def __init__(self):
        self.problems = {}
        self.last_problem_key = 0
    
    def add_problem(self, problem):
        self.last_problem_key += 1
        self.problems[self.last_problem_key] = problem
        return self.last_problem_key
    
    def delete_problem(self, problem_key):
        if problem_key in self.problems:
            del self.problems[problem_key]

    def get_problem(self, problem_key):
        problem = self.problems.get(problem_key)
        if problems is None:
            return None
        problem_ = Problem(problem.name, problem.url, problem.difficulty)
        return problem_
    
    def get_problems(self):
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty)
            problems.append((problem_key, problem_))
        return problems