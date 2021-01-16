class Problem:
    def __init__(self, name, url, difficulty, topics, owner_id, likes=0, dislikes=0):
        self.name = name
        self.url = url
        self.difficulty = difficulty
        self.topics = []
        self.owner_id = owner_id
        self.likes = likes
        self.dislikes = dislikes
        for topic in topics:
            self.topics.append(topic)
