from pydantic import BaseModel , EmailStr , Field

class EmailUserSchema(
    BaseModel
):
    email : EmailStr = Field(
        examples=["medin@gmail.com"]
    )
    
class PasswordUserSchema(
    BaseModel
):
    
    password : str = Field(
        title="your password",
        min_length=5,
        examples=["your secret password"],
    )

class LoginUserSchema(
    EmailUserSchema,
    PasswordUserSchema
):
    pass
    
class RegisterUserSchema(
    LoginUserSchema
):
    name : str = Field(
        title="username",
        min_length=1,
        examples=["Pedro Henrique"]
    )
    
class VerifyTokenSchema(
    BaseModel
):
    token : str
    