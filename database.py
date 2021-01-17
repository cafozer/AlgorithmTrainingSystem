from problem import Problem
from topic import Topic
from problem_topic_rel import Problem_topic_rel
import psycopg2
import psycopg2.extras

class Database:
    def __init__(self):
        self.users = {}
        self.last_user_key = 0
        self.problems = {}
        self.last_problem_key = 0
        self.topics = {"dfs-and-similar", "graph-theory", "math", "dynamic-programming"}
        self.last_topic_key = 0
        self.problem_topic_rels = []
        self.status = []

    def add_user(self, user):
        self.last_user_key += 1
        self.users[self.last_user_key] = user
        return self.last_user_key

    def add_problem(self, problem):
        self.last_problem_key += 1
        self.problems[self.last_problem_key] = problem
        return self.last_problem_key
    
    def delete_problem(self, problem_key):
        if problem_key in self.problems:
            del self.problems[problem_key]

    def get_problem(self, problem_key):
        problem = self.problems.get(problem_key)
        if problem is None:
            return None
        problem_ = Problem(problem.name, problem.url, problem.difficulty)
        return problem_
    
    def get_problems(self):
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            print(problem_.url)
            problems.append((problem_key, problem_))
        return problems

    def add_topic(self, topic):
        self.last_topic_key +=1
        self.topics[self.last_topic_key] = topic
        return self.last_topic_key
    
    def add_problem_topic_rel(self, topic_id, problem_id):
        self.problem_topic_rels.append((topic_id, problem_id))

    def add_status(self, status_):
        self.status.append(status)

    def find_weak_topics(self, user_id_):
        weakness = {}
        for statu in self.status:
            if statu.user_id == user_id and statu.solved == 0:
                if weakness[self.get_problem(statu.problem_id)] > 0:
                    weakness[self.get_problem(statu.problem_id)] += 1
                else:
                    weakness[self.get_problem(statu.problem_id)] = 1

        sorted_weakness = dict(sorted(weakness.items()), key=lambda item: item[1])
        return sorted_weakness[0:3]


    def get_efficient_problems(self, topic_id):
        problemset_ = []
        for topic_id_, problem_id_ in self.problem_topic_rels:
            if topic_id == topic_id_:
                problemset_.append((self.get_problem(problem_id_).likes-self.get_problem(problem_id_).dislikes, problem_id_))
        problemset_.sort(reverse=True)
        return problemset_[0:2]

    def list_by_topic(self, topic_id):
        problems_ = []
        for topic_id_, problem_id_ in self.problem_topic_rels:
            if topic_id == topic_id_:
                problems_.append(self.get_problem(problem_id_))
        return problems_

    def sort_by_likes(self):
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            problems.append((problem.likes-problem.dislikes, problem_key, problem_))
        problems.sort(reverse=True)
        problems_ = [prob[1:] for prob in problems]
        return problems_

    def sort_by_difficulty_ascending(self):
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            problems.append((problem.difficulty, problem_key, problem_))
        problems.sort()
        problems_ = [prob[1:] for prob in problems]
        return problems_

    def sort_by_difficulty_descending(self):
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            print(problem_.url)
            problems.append((problem.difficulty, problem_key, problem_))
        problems.sort(reverse=True)
        problems_ = [prob[1:] for prob in problems]
        return problems_     