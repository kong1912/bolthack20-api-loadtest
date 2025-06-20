from locust import HttpUser, task, between, TaskSet, SequentialTaskSet
import uuid
import random

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSIsImV4cCI6MTc1MDQxNjEyOSwiaWF0IjoxNzUwMzk0NTI5LCJuYmYiOjE3NTAzOTQ1MjksInJvbGUiOiJhZG1pbiIsInVzZXJfaWQiOiIzMGVmNDYzMS1lYzlkLTQzZDEtYWI5NS1hYTU1NTNhNzEzODgifQ.jgbOU12FwqBowDqJPscOtBnHSUy14jZWAO0iLqXTAHY"
AUTH_HEADER = {"Authorization": f"Bearer {TOKEN}"}

class AuthTasks(SequentialTaskSet):
    def on_start(self):
        self.email = f"user_{uuid.uuid4().hex[:8]}@fortest.com"
        print(f"Generated email: {self.email}")
        self.password = "123456"
    @task
    def get_welcome_message(self):
        self.client.get("/")

    @task
    def signup(self):
        with self.client.post("/auth/signup", json={
            "email": self.email,
            "password": self.password
        }, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            elif response.status_code == 409:
                try:
                    data = response.json()
                    if "already exists" in str(data):
                        response.success()
                    else:
                        response.failure(str(data))
                except Exception:
                    if "already exists" in response.text:
                        response.success()
                    else:
                        response.failure(response.text)
            else:
                response.failure(f"Unexpected status: {response.status_code} {response.text}")

    @task
    def signin(self):
        with self.client.post("/auth/signin", json={
            "email": self.email,
            "password": self.password
        }, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.user.uid = data.get("user_id")
                except Exception:
                    self.user.uid = None

class UserTasks(SequentialTaskSet):
    def on_start(self):
        self.user_ids = []

    @task
    def get_all_users(self):
        with self.client.get("/api/users/", headers=AUTH_HEADER) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.user_ids = [u.get("user_id") for u in data]
                except Exception:
                    self.user_ids = []

    @task
    def get_user_by_id(self):
        if self.user_ids:
            uid = random.choice(self.user_ids)
        else:
            uid = getattr(self.user, "uid", "123")
        self.client.get(f"/api/users/{uid}", headers=AUTH_HEADER, name="/api/users/:id")

    @task
    def create_user(self):
        self.client.post("/api/users/create", json={
            "email": f"newuser_{uuid.uuid4().hex[:8]}@example.com",
            "password": "123456"
        }, headers=AUTH_HEADER)

    @task
    def update_user_by_id(self):
        if self.user_ids:
            uid = random.choice(self.user_ids)
        else:
            uid = getattr(self.user, "uid", "123")
        self.client.put(f"/api/users/{uid}", json={
            "email": "updated@example.com",
            "password": "654321",
        }, headers=AUTH_HEADER, name="/api/users/:id")

    @task
    def delete_user_by_id(self):
        if self.user_ids:
            uid = random.choice(self.user_ids)
        else:
            uid = getattr(self.user, "uid", "123")
        self.client.delete(f"/api/users/{uid}", headers=AUTH_HEADER, name="/api/users/:id")

class ChatTasks(SequentialTaskSet):
    def on_start(self):
        self.chat_ids = []

    @task
    def get_all_chats(self):
        with self.client.get("/api/chats/", headers=AUTH_HEADER) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.chat_ids = [c.get("chat_id") or c.get("id") or c.get("chatId") for c in data]
                except Exception:
                    self.chat_ids = []

    @task
    def create_chat(self):
        with self.client.post("/api/chats/", json={
            "text": "Hello world!"
        }, headers=AUTH_HEADER) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    chat_id = data.get("chat_id") or data.get("id") or data.get("chatId")
                    self.user.chat_id = chat_id
                    if chat_id:
                        self.chat_ids.append(chat_id)
                except Exception:
                    self.user.chat_id = "456"
            else:
                self.user.chat_id = "456"

    @task
    def get_chat_by_id(self):
        if self.chat_ids:
            chat_id = random.choice(self.chat_ids)
        else:
            chat_id = getattr(self.user, "chat_id", "456")
        self.client.get(f"/api/chats/getByChatID/{chat_id}", headers=AUTH_HEADER, name="/api/chats/:id")

    @task
    def update_chat_by_id(self):
        if self.chat_ids:
            chat_id = random.choice(self.chat_ids)
        else:
            chat_id = getattr(self.user, "chat_id", "456")
        self.client.put(f"/api/chats/{chat_id}", json={
            "message": "Updated message"
        }, headers=AUTH_HEADER, name="/api/chats/:id")

    @task
    def delete_chat_by_id(self):
        if self.chat_ids:
            chat_id = random.choice(self.chat_ids)
        else:
            chat_id = getattr(self.user, "chat_id", "456")
        self.client.delete(f"/api/chats/{chat_id}", headers=AUTH_HEADER, name="/api/chats/:id")

    @task
    def get_all_chat_ids(self):
        self.client.get("/api/chats/all_chat_id", headers=AUTH_HEADER)

class WebsiteUser(HttpUser):
    host = "https://healthcare-0y63.onrender.com"
    wait_time = between(1, 5)
    tasks = [AuthTasks, UserTasks, ChatTasks]