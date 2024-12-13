from uuid import UUID


class User:

    id: UUID
    name: str
    email: str
    phone_number: str
    password: str

    def __init__(self, id: UUID, name: str, email: str, phone_number: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.validate()

    
    def validate(self):
        if not isinstance(self.id, UUID):
            raise Exception("id must be an UUID")
        
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise Exception("name is required")
        
        if not isinstance(self.email, str) or len(self.email) == 0:
            raise Exception("email is required")
        
        if not isinstance(self.phone_number, str) or len(self.phone_number) == 0:
            raise Exception("phone_number is required")
        
        if not isinstance(self.password, str) or len(self.password) <= 4:
            raise Exception("password is required and length must be greater than 4")
        