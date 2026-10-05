from pydantic import BaseModel,EmailStr,Field,field_validator
class Register(BaseModel): name:str=Field(min_length=2,max_length=120); email:EmailStr; password:str=Field(min_length=8,max_length=128)
class Login(BaseModel): email:EmailStr; password:str=Field(min_length=8,max_length=128)
class VersionIn(BaseModel):
    problem:str=Field(min_length=20,max_length=5000); solution:str=Field(min_length=20,max_length=5000); target_users:str=Field(min_length=3,max_length=2000); features:list[str]=Field(min_length=1,max_length=30); impact:str=Field(min_length=10,max_length=3000); technology_preference:str|None=None; team_size:int=Field(ge=1,le=50); team_skill_level:str=Field(pattern="^(beginner|intermediate|advanced)$"); hackathon_duration_hours:int=Field(ge=1,le=720); prototype:str|None=None; constraints:str|None=None
    @field_validator("features")
    @classmethod
    def features_clean(cls,v):
        v=[x.strip() for x in v if x.strip()];
        if not v: raise ValueError("At least one feature is required")
        return v
class CreateIdea(BaseModel): title:str=Field(min_length=3,max_length=200); version:VersionIn
class Score(BaseModel): score:float=Field(ge=0,le=100); confidence:str=Field(pattern="^(High|Medium|Low)$"); explanation:str; evidence:list[str]; improvement:str
