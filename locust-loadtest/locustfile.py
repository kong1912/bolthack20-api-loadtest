from locust import HttpUser, task, between, SequentialTaskSet, tag, TaskSet, LoadTestShape
import uuid

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSIsImV4cCI6MTc1MTg1NDcxMSwiaWF0IjoxNzUwNjQ1MTExLCJuYmYiOjE3NTA2NDUxMTEsInJvbGUiOiJhZG1pbiIsInVzZXJfaWQiOiIwMGVlODcwZi04MzYyLTQ1NDMtYWIxZS05ODc4NWE3N2Q4Y2UifQ.tVM7xoy1BAcO6eqvTmpAIhl770yql9qSqet8ZSTu51w"
AUTH_HEADER = {"Authorization": f"Bearer {TOKEN}"}

USER_ID = "420a247f-36eb-467e-80c2-d056af958172"
CHAT_ID = "beaec2fb-fe23-4c3d-b095-a0d9a147e757"

class AuthTasks(SequentialTaskSet):
    def on_start(self):
        self.password = "123456"
        # self.email = f"user_{uuid.uuid4().hex[:8]}@fortest.com"

    @task
    @tag("signup")
    def signup(self):
        self.email = f"user_{uuid.uuid4().hex[:8]}@fortest.com"
        print(f"[signup] Email: {self.email}, Password: {self.password}")
        with self.client.post("/auth/signup", json={
            "email": self.email,
            "password": self.password
        }, catch_response=True) as response:
            if response.status_code in [200, 201, 409]:
                response.success()
                self.schedule_task(self.signin)  # Schedule signin after signup
            else:
                print(f"[signup] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    def signin(self):
        print(f"[signin] Email: {self.email}, Password: {self.password}")
        with self.client.post("/auth/signin", json={
            "email": self.email,
            "password": self.password
        }, catch_response=True) as response:
            if response.status_code != 200:
                print(f"[signin] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

class UserTasks(TaskSet):
    @task
    @tag("users", "get_all")
    def get_all_users(self):
        with self.client.get("/api/users/", headers=AUTH_HEADER, catch_response=True) as response:
            if response.status_code != 200:
                print(f"[get_all_users] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    @task
    @tag("users", "get_by_id")
    def get_user_by_id(self):
        with self.client.get(f"/api/users/{USER_ID}", headers=AUTH_HEADER, name="/api/users/:id", catch_response=True) as response:
            if response.status_code != 200:
                print(f"[get_user_by_id] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    @task
    @tag("users", "create")
    def create_user(self):
        with self.client.post("/api/users/create", json={
            "email": f"newuser_{uuid.uuid4().hex[:8]}@example.com",
            "password": "123456"
        }, headers=AUTH_HEADER, catch_response=True) as response:
            if response.status_code != 201:
                print(f"[create_user] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

class ChatTasks(TaskSet):
    @task
    @tag("chats", "get_all")
    def get_all_chats(self):
        with self.client.get("/api/chats/", headers=AUTH_HEADER, catch_response=True) as response:
            if response.status_code != 200:
                print(f"[get_all_chats] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    @task
    @tag("chats", "create")
    def create_chat(self):
        with self.client.post("/api/chats/", json={
            "message": "Hello world!",
            "receiver_id": "789"
        }, headers=AUTH_HEADER, catch_response=True) as response:
            if response.status_code != 201:
                print(f"[create_chat] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    @task
    @tag("chats", "get_by_id")
    def get_chat_by_id(self):
        with self.client.get(f"/api/chats/getByChatID/{CHAT_ID}", headers=AUTH_HEADER, name="/api/chats/:id", catch_response=True) as response:
            if response.status_code != 200:
                print(f"[get_chat_by_id] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    @task
    @tag("chats", "get_all_ids")
    def get_all_chat_ids(self):
        with self.client.get("/api/chats/all_chat_id", headers=AUTH_HEADER, catch_response=True) as response:
            if response.status_code != 200:
                print(f"[get_all_chat_ids] Error: {response.status_code} {response.text}")
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

class WebsiteUser(HttpUser):
    host = "https://healthcare-0y63.onrender.com"
    wait_time = between(1, 10)
    tasks = [AuthTasks, UserTasks, ChatTasks]

class StepLoadShape(LoadTestShape):
    """
    A step load shape that
    - starts at 5 users,
    - increases by 5 users every 1 minute,
    - up to a maximum of 50 users.
    """
    step_time = 60        # seconds per step
    step_users = 5        # users to add each step
    max_users = 50        # maximum users
    spawn_rate = 5        # users to spawn per second

    def tick(self):
        run_time = self.get_run_time()
        current_step = int(run_time // self.step_time)
        user_count = min(self.step_users * (current_step + 1), self.max_users)
        if user_count > self.max_users:
            return None
        return (user_count, self.spawn_rate)