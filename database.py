from problem import Problem
from topic import Topic
from user import User
from problem_topic_rel import Problem_topic_rel
import psycopg2
import psycopg2.extras
from collections import defaultdict
import os
import sys

class Database:
    def __init__(self):
        """
        self.users = {}
        self.last_user_key = 0
        self.problems = {}
        self.last_problem_key = 0
        self.topics = {0:Topic("dfs-and-similar"), 1:Topic("graph-theory"), 2:Topic("math"), 3:Topic("dynamic-programming")}
        self.last_topic_key = 3
        self.problem_topic_rels = []
        self.status = []
        """
        self.url = os.getenv("DATABASE_URL")
        #self.connection = psycopg2.connect(self.url)
        #self.cur = self.connection.cursor()

    def add_user(self, user):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO USER_TABLE (number_of_questions_added, dislikes, username, likes, user_password) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(statement, [user.number_of_questions_added, user.number_of_dislikes, user.username, user.number_of_likes, user.password])
                cursor.close()
                return user
        except Exception as err:
            print("Error: ", err)
            return None

    def get_user(self, username):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM USER_TABLE WHERE username = %s"
                cursor.execute(statement, [username])
                result = cursor.fetchone()
                cursor.close()
                if result is None:
                    return None
                else:
                    return User(result[1], result[2], result[3], result[4], result[5])
        except Exception as err:
            print("Error: ", err)

    def get_users_by_like(self):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM user_table"
                cursor.execute(statement)
                users = cursor.fetchall()
                cursor.close()
                ret = []
                for key, username, dummy, number_of_questions, likes, dislikes in users:
                    ret.append((likes-dislikes, username))
                ret.sort(reverse=True)
                ret_ = [u[1:] for u in ret]
                return ret_
        except Exception as err:
            print("Error: ", err)


    def get_user_key(self, username):
        """
        for key, name in self.users:
            if name == username:
                return key
        return None
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT user_id FROM user_table WHERE username = %s"
                cursor.execute(statement, [username])
                ret = cursor.fetchone()[0]
                cursor.close()
                return ret
        except Exception as err:
            print("Error: ", err)

    def add_problem(self, problem):
        """
        self.last_problem_key += 1
        self.problems[self.last_problem_key] = problem
        self.problems[self.last_problem_key].key = self.last_problem_key
        problem.key = self.last_problem_key
        return self.last_problem_key
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO problem (problem_name, url, difficulty_level, number_of_likes, number_of_dislikes, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, [problem.name, problem.url, problem.difficulty, problem.likes, problem.dislikes, problem.owner_id])
                statement = "SELECT problem_id FROM problem WHERE problem_name = %s"
                cursor.execute(statement, [problem.name])
                ret = cursor.fetchone()[0]
                cursor.close()
                return ret
        except Exception as err:
            print("Error: ", err)
            return None
    
    def delete_problem(self, problem_name):
        """
        if problem_key in self.problems:
            del self.problems[problem_key]
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM problem WHERE problem_name = %s"
                cursor.execute(statement, [problem_name])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def get_problem(self, problem_key):
        """
        problem = self.problems.get(problem_key)
        if problem is None:
            return None
        return problem
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM problem WHERE problem_id = %s"
                cursor.execute(statement, [problem_key])
                problem_ = cursor.fetchone()
                cursor.close()
                return Problem(problem_[1], problem_[2], problem_[3], problem_[6], problem_[4], problem_[5])
        except Exception as err:
            print("Error: ", err)
            
    
    def get_problems(self):
        """
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            problems.append((problem_key, problem_))
        return problems
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM problem"
                cursor.execute(statement)
                problems_from_db = cursor.fetchall()
                cursor.close()
                problems = []
                for key, name, url, difficulty, likes, dislikes, owner_key in problems_from_db:
                    problem_ = Problem(name, url, difficulty, owner_key, likes, dislikes)
                    problems.append((key, problem_))
                problems.sort()
                return problems
        except Exception as err:
            print("Error: ", err)

    def get_problem_key(self, problem_name):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT problem_id FROM problem WHERE problem_name = %s"
                cursor.execute(statement, [problem_name])
                ret = cursor.fetchone()[0]
                cursor.close()
                return ret
        except Exception as err:
            print("Error: ", err)

    def give_like(self, probkey):
        """
        problem = self.problems.get(probkey)
        problem.likes += 1
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE problem SET number_of_likes = number_of_likes+1 WHERE problem_id = %s"
                cursor.execute(statement, [probkey])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def give_dislike(self, probkey):
        """
        problem = self.problems.get(probkey)
        problem.dislikes += 1
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE problem SET number_of_dislikes = number_of_dislikes+1 WHERE problem_id = %s"
                cursor.execute(statement, [probkey])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def add_topic(self, topic):
        """
        self.last_topic_key +=1
        self.topics[self.last_topic_key] = topic
        return self.last_topic_key
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO topic (topic_name) VALUES (%s)"
                cursor.execute(statement, [topic.name])
                cursor.close()
                return topic
        except Exception as err:
            print("Error: ", err)
            return None

    def get_topic(self, key):
        """
        topic = self.topics.get(int(key))
        if topic is None:
            return None
        return topic
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT topic_name FROM topic WHERE topic_id = %s"
                cursor.execute(statement, [key])
                name = cursor.fetchone()[0]
                cursor.close()
                return Topic(name)
        except Exception as err:
            print("Error: ", err)

    def give_topics(self):
        """
        ret = []
        for key, topic in self.topics.items():
            ret.append((key, topic.name))
        return ret
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM topic"
                cursor.execute(statement)
                f = cursor.fetchall()
                cursor.close()
                ret = []
                for key, name in f:
                    ret.append((key, name))
                return ret
        except Exception as err:
            print("Error: ", err)
    
    def add_problem_topic_rel(self, topic_id, problem_id):
        """
        self.problem_topic_rels.append((topic_id, problem_id))
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO problemtopicrelation (problem_id, topic_id) VALUES (%s, %s)"
                cursor.execute(statement, [problem_id, topic_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def give_rels(self):
        """
        return self.problem_topic_rels
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * from problemtopicrelation"
                cursor.execute(statement)
                rels = cursor.fetchall()
                cursor.close()
                return rels
        except Exception as err:
            print("Error: ", err)

    def add_status(self, status_):
        """
        self.status.append(status_)
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM STATUS WHERE problem_id = %s AND user_id = %s"
                cursor.execute(statement, [status_.problem_id, status_.user_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO STATUS (problem_id, user_id, solved) VALUES (%s, %s, %s)"
                cursor.execute(statement, [status_.problem_id, status_.user_id, status_.solved])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def find_weak_topics(self, user_id):
        """
        weakness = {}
        for statu in self.status:
            if statu.user_id == user_id and statu.solved == 0:
                if weakness[self.get_problem(statu.problem_id)] > 0:
                    weakness[self.get_problem(statu.problem_id)] += 1
                else:
                    weakness[self.get_problem(statu.problem_id)] = 1

        sorted_weakness = dict(sorted(weakness.items()), key=lambda item: item[1])
        return sorted_weakness[0:3]
        """
        try:
            weakness = {}
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT problem_id FROM status WHERE user_id = %s AND solved = 0"
                cursor.execute(statement, [user_id])
                cannot_solved_problems = cursor.fetchall()
                for problem_id in cannot_solved_problems:
                    statement = "SELECT topic_id FROM problemtopicrelation WHERE problem_id = %s"
                    cursor.execute(statement, [problem_id[0]])
                    weak_topics = cursor.fetchall()
                    for weak_topic in weak_topics:
                        cur = weakness.get(weak_topic[0])
                        if cur:
                            weakness[weak_topic[0]] += 1
                        else:
                            weakness[weak_topic[0]] = 1
                cursor.close()
                sorted_weakness = dict(sorted(weakness.items(), key=lambda item: item[1], reverse=True))
                ret = []
                for a, b in sorted_weakness.items():
                    ret.append((a,b))
                return ret[0:3]
        except Exception as err:
            print("Error: ", err)

    def get_efficient_problems(self, topic_id):
        """
        problemset_ = []
        for topic_id_, problem_id_ in self.problem_topic_rels:
            if topic_id == topic_id_:
                problemset_.append((self.get_problem(problem_id_).likes-self.get_problem(problem_id_).dislikes, problem_id_))
        problemset_.sort(reverse=True)
        return problemset_[0:2]
        """
        try:
            efficient_problems = []
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT problem_id FROM problemtopicrelation WHERE topic_id = %s"
                cursor.execute(statement, [topic_id])
                ids = cursor.fetchall()
                for prob_id in ids:
                    problem_ = self.get_problem(prob_id[0])
                    efficient_problems.append((problem_.likes-problem_.dislikes, prob_id[0]))
                cursor.close()
                efficient_problems.sort(reverse=True)
                ret = [prob[1:2] for prob in efficient_problems]
                return ret[0:2]
        except Exception as err:
            print("Error: ", err)

    def sort_by_likes(self):
        """
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            problems.append((problem.likes-problem.dislikes, problem_key, problem_))
        problems.sort(reverse=True)
        problems_ = [prob[1:] for prob in problems]
        return problems_
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM problem"
                cursor.execute(statement)
                problems_from_db = cursor.fetchall()
                cursor.close()
                problems = []
                for key, name, url, difficulty, likes, dislikes, owner_key in problems_from_db:
                    problem_ = Problem(name, url, difficulty, owner_key, likes, dislikes)
                    problems.append((likes-dislikes,key, problem_))
                problems.sort(reverse=True)
                problems_ = [prob[1:] for prob in problems]
                return problems_
        except Exception as err:
            print("Error: ", err)

    def sort_by_difficulty_ascending(self):
        """
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            problems.append((problem.difficulty, problem_key, problem_))
        problems.sort()
        problems_ = [prob[1:] for prob in problems]
        return problems_
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM problem"
                cursor.execute(statement)
                problems_from_db = cursor.fetchall()
                cursor.close()
                problems = []
                for key, name, url, difficulty, likes, dislikes, owner_key in problems_from_db:
                    problem_ = Problem(name, url, difficulty, owner_key, likes, dislikes)
                    problems.append((difficulty,key, problem_))
                problems.sort()
                problems_ = [prob[1:] for prob in problems]
                return problems_
        except Exception as err:
            print("Error: ", err)

    def sort_by_difficulty_descending(self):
        """
        problems = []
        for problem_key, problem in self.problems.items():
            problem_ = Problem(problem.name, problem.url, problem.difficulty, problem.owner_id, problem.likes, problem.dislikes)
            problems.append((problem.difficulty, problem_key, problem_))
        problems.sort(reverse=True)
        problems_ = [prob[1:] for prob in problems]
        return problems_     
        """
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM problem"
                cursor.execute(statement)
                problems_from_db = cursor.fetchall()
                cursor.close()
                problems = []
                for key, name, url, difficulty, likes, dislikes, owner_key in problems_from_db:
                    problem_ = Problem(name, url, difficulty, owner_key, likes, dislikes)
                    problems.append((difficulty,key, problem_))
                problems.sort(reverse=True)
                problems_ = [prob[1:] for prob in problems]
                return problems_
        except Exception as err:
            print("Error: ", err)

    def increase_number_of_questions(self, owner_id):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE user_table SET number_of_questions_added = number_of_questions_added+1 WHERE user_id = %s"
                cursor.execute(statement, [owner_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def decrease_number_of_questions(self, owner_name):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE user_table SET number_of_questions_added = number_of_questions_added-1 WHERE username = %s"
                cursor.execute(statement, [owner_name])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def increase_likes(self, owner_id):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE user_table SET likes = likes+1 WHERE user_id = %s"
                cursor.execute(statement, [owner_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def decrease_likes(self, number, ownername):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE user_table SET likes = likes-%s WHERE username = %s"
                cursor.execute(statement, [number, ownername])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def increase_dislikes(self, owner_id):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE user_table SET dislikes = dislikes+1 WHERE user_id = %s"
                cursor.execute(statement, [owner_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def decrease_dislikes(self, number, ownername):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE user_table SET dislikes = dislikes-%s WHERE username = %s"
                cursor.execute(statement, [number, ownername])
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def get_problems_of_a_user(self, username):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM problem WHERE user_id = %s"
                cursor.execute(statement, [self.get_user_key(username)])
                problems_from_db = cursor.fetchall()
                cursor.close()
                problems = []
                for key, name, url, difficulty, likes, dislikes, owner_key in problems_from_db:
                    problem_ = Problem(name, url, difficulty, owner_key, likes, dislikes)
                    problems.append((key, problem_))
                problems.sort()
                return problems
        except Exception as err:
            print("Error: ", err)

    def update_problem(self, updated_problem, old_name):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT problem_id FROM problem WHERE problem_name = %s"
                cursor.execute(statement, [old_name])
                ret = cursor.fetchone()[0]
                statement = "UPDATE problem SET problem_name = %s, url = %s, difficulty_level = %s WHERE problem_id = %s"
                cursor.execute(statement, [updated_problem.name, updated_problem.url, updated_problem.difficulty, ret])
                cursor.close()
                return ret
        except Exception as err:
            print("Error: ", err)

    def delete_relations(self, problem_id):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM problemtopicrelation WHERE problem_id = %s"
                cursor.execute(statement, [problem_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)
    
    def delete_status(self, problem_id):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM status WHERE problem_id = %s"
                cursor.execute(statement, [problem_id])
                cursor.close()
        except Exception as err:
            print("Error: ", err)
            
    def give_total_problems(self):
        try:
            with psycopg2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT SUM(number_of_questions_added) FROM user_table"
                cursor.execute(statement)
                ret = cursor.fetchone()[0]
                cursor.close()
                return ret
        except Exception as err:
            print("Error: ", err)