class SimpleEnv:
    def __init__(self):
        self.tasks = [
            {"state": "hungry", "correct": "eat"},
            {"state": "tired", "correct": "sleep"},
            {"state": "exam", "correct": "study"}
        ]
        self.current = 0

    def reset(self):
        self.current = 0
        return self.tasks[self.current]["state"]

    def step(self, action):
        if self.current >= len(self.tasks):
            return None, 0.0, True, {}

        task = self.tasks[self.current]
        correct = task["correct"]

        reward = 1.0 if action.lower() == correct else 0.0

        self.current += 1
        done = self.current >= len(self.tasks)

        next_state = None if done else self.tasks[self.current]["state"]

        return next_state, reward, done, {}