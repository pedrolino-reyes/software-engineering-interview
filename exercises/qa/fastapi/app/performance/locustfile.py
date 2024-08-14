import time
from locust import HttpUser, task, between

class TaskPerformance(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_tasks(self):
        self.client.get("/tasks")

    # @task
    # def get_task_by_id(self):
    #     self.client.get("/tasks/1")
