from config import API_BASE_URL


class UsersAPI:
    def __init__(self, api_request_context):
        self.request = api_request_context
        self.base_url = f"{API_BASE_URL}/api/users"

    def get_users(self, headers=None):
        return self.request.get(self.base_url, headers=headers)

    def create_user(self, payload):
        return self.request.post(self.base_url, data=payload)

    def get_user(self, user_id):
        return self.request.get(f"{self.base_url}/{user_id}")

    def update_user(self, user_id, payload):
        return self.request.put(f"{self.base_url}/{user_id}", data=payload)

    def delete_user(self, user_id):
        return self.request.delete(f"{self.base_url}/{user_id}")