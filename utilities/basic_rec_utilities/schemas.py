import json

class UserActivity:
    """
    v1: { 'user': ___, 'activity': [{'interaction': ___, 'items': [___,___]}, ...] }
    """
    def __init__(self, data:dict, schema_version:str = "v1") -> None:
        self.user = data.get("user")
        self.activity = data.get("activity")
        pass
    
    def to_json(self, schema_version:str = "v1") -> json:
        """
        """
        return {
            "user": self.user,
            "activity": self.activity
        }

class UserActivityIngested:
    """
    v1: { 'users': [___, ...]}
    """
    def __init__(self, data:dict, schema_version:str = "v1") -> None:
        self.users = data.get("users")
        pass
    
    def to_json(self, schema_version:str = "v1") -> json:
        """
        """
        return {
            "users": self.users
        }