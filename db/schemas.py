from pydantic import BaseModel, Field, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserParse:
    def __init__(self,user):
        self.user = user

    async def parsedata(self) -> dict:
        parsed_data = {}
        for key in self.user.keys():
            if key == "_id":
                parsed_data["id"] = str(self.user[key])
            else:
                if key == "password":
                    continue
                else:
                    parsed_data[key] = self.user[key]
        return parsed_data