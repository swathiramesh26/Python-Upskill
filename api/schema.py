"""
schema.py
JSON Schemas describe the expected contents of reqres.in api responses.
"""

# Single user object, as returned inside "data" for GET /users/:id
USER_SCHEMA = {
    "title": "User",
    "type": "object",
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string", "format": "email"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string", "pattern": "^https?://"},
    },
    "additionalProperties": True,
}

# GET /users?page=2  (paginated list)
GET_USERS_LIST_SCHEMA = {
    "title": "UserList",
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data", "support"],
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": USER_SCHEMA,
        },
        "support": {"type": "object"},
    },
}

# GET /users/:id  (single user wrapper)
GET_SINGLE_USER_SCHEMA = {
    "title": "SingleUser",
    "type": "object",
    "required": ["data", "support"],
    "properties": {
        "data": USER_SCHEMA,
        "support": {"type": "object"},
    },
}

# POST /users  (create)
CREATE_USER_SCHEMA = {
    "title": "CreateUser",
    "type": "object",
    "required": ["name", "job", "id", "createdAt"],
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"},
        "createdAt": {"type": "string"},
    },
}

# PUT /users/:id  (update)
UPDATE_USER_SCHEMA = {
    "title": "UpdateUser",
    "type": "object",
    "required": ["name", "job", "updatedAt"],
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "updatedAt": {"type": "string"},
    },
}