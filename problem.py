class Problem:
    def __init__(self, name, url, difficulty, owner_id, likes=0, dislikes=0):
        self.key = None
        self.name = name
        self.url = url
        self.difficulty = difficulty
        self.topics = []
        self.owner_id = owner_id
        self.likes = likes
        self.dislikes = dislikes
