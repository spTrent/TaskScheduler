from dataclasses import dataclass
import random
from ..contracts.task import Task
from datetime import timedelta, datetime

@dataclass
class GeneratorSource:
    payload_variants = ['Сделать лабу, сходить в зал, пройти урок по английскому, приготовить ужин']
    deadline_variants = [timedelta(days=1), timedelta(days=2), timedelta(days=3), timedelta(hours=8), timedelta(hours=2)]
    def get_task(self) -> Task:
        id = random.randint(0, 100)
        payload = random.choice(self.payload_variants)
        deadline = datetime.now() + random.choice(self.deadline_variants)
        return Task(id=id, payload=payload, deadline=deadline)
    
