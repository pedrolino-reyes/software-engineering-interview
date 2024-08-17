import random
import string

from locust import HttpUser, task, between

# we might not want to generate data in a real performance test, since it will take up
# processing time
def generate_random_string():
    length = random.randint(1, 10)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_text(number_of_strings):
    text = ""
    for i in range(number_of_strings):
        text += generate_random_string() + " "
    return text.strip()


def generate_title():
    return generate_text(random.randint(3, 5))


def generate_description():
    return generate_text(random.randint(10, 20))


class TaskPerformance(HttpUser):
    """
    Locust simulation to test the performance of the Tasklist web app.
    """
    wait_time = between(1, 5)

    @task
    def get_tasks(self):
        self.client.get("/tasks/")

    @task(10)
    def create_task(self):
        payload = {
            "title": generate_title(),
            "description": generate_description()
        }
        self.client.post("/tasks/", json=payload)
