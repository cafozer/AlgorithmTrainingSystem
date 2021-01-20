import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
    "DROP TABLE IF EXISTS ProblemTopicRelation CASCADE",
    "DROP TABLE IF EXISTS Topic CASCADE",
    "DROP TABLE IF EXISTS Status CASCADE",
    "DROP TABLE IF EXISTS Problem CASCADE",
    "DROP TABLE IF EXISTS USER_TABLE CASCADE",

    """CREATE TABLE IF NOT EXISTS USER_TABLE(
    User_ID                       			SERIAL,
    Username                      		VARCHAR(30) UNIQUE NOT NULL,
    User_password							VARCHAR(200) NOT NULL,
    Number_of_questions_added     	INT NOT NULL,
    Likes                        			INT NOT NULL,
    Dislikes                      			INT NOT NULL,
    PRIMARY KEY (User_ID)
)""",

"""CREATE TABLE IF NOT EXISTS Problem
(
  problem_id                   		SERIAL,
  problem_name                             VARCHAR(30) UNIQUE NOT NULL,
  URL                           			VARCHAR(200) NOT NULL,
  Difficulty_level              		VARCHAR(10) NOT NULL,
  Number_of_likes               		INT NOT NULL,
  Number_of_dislikes           		INT NOT NULL,
  User_ID				INT NOT NULL,
  PRIMARY KEY (problem_ID),
  FOREIGN KEY (User_ID)
    REFERENCES user_table(User_ID)
)""",

"""CREATE TABLE IF NOT EXISTS Status
(
  problem_ID                   		INT NOT NULL,
  User_ID                       			INT NOT NULL,
  Solved                        			INT,
  PRIMARY KEY (problem_ID, User_ID),
  FOREIGN KEY (User_ID) 
    REFERENCES user_table(User_ID),
  FOREIGN KEY (problem_ID) 
    REFERENCES problem(problem_ID)
)""",

"""CREATE TABLE IF NOT EXISTS Topic
(
  Topic_ID                      			SERIAL,
  Topic_name                    		VARCHAR(30) UNIQUE NOT NULL,
  PRIMARY KEY (Topic_ID)
)""",

"""CREATE TABLE IF NOT EXISTS ProblemTopicRelation
(
  Problem_ID                   		INT NOT NULL,
  Topic_ID                      			INT NOT NULL,
  PRIMARY KEY (problem_ID, Topic_ID),
  FOREIGN KEY (problem_ID) 
    REFERENCES problem(problem_ID),
  FOREIGN KEY (Topic_ID) 
    REFERENCES Topic(Topic_ID)
)""",
]

def initialize(url):
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in INIT_STATEMENTS:
                cursor.execute(statement)
            cursor.close()
    except Exception as err:
        print("Error: ", err)

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)