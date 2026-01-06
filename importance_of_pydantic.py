from pydantic import BaseModel,EmailStr,AnyUrl,StrictFloat,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

#nested pydantic model 
class contactDetails(BaseModel):
    email:EmailStr
    phone:int
    emergency:str

    # @field_validator("contact_details",mode="before")
    # @classmethod

    # def email_validator(cls,value):
    #     valid_domain=['hdfc.com','icic.com']
    #     email=value.get("email")
    #     domain_name=email.split('@')[-1]

    #     if(domain_name not in valid_domain):
    #         raise ValueError("not a valid domain ")
    #     return value

class patient(BaseModel):
    # name:str=Field(max_length=42)
    name:Annotated[str,Field(max_length=42,description="in this we write a nem of the person",examples=['Taniya','Choudhary'])]
    age:int
    github_url:AnyUrl
    weight: StrictFloat=Field(gt=0)
    height: StrictFloat = Field(gt=0, description="Height in meters")  # ✅ Added height
    # married:Optional[bool]=None
    married:Annotated[Optional[bool],Field(default=None,description='is the patient married')]
    allergies:List[str]
    contact_details:contactDetails

    @model_validator(mode='after')

    def validate_emergecy_contact(cls,model):
        if model.age>60 and not model.contact_details.emergency:
            raise ValueError('patient older than 60 must have an emergency contact_details ')
        return  model

    @field_validator("contact_details",mode="before")
    @classmethod

    def email_validator(cls,value):
        valid_domain=['hdfc.com','icic.com']
        email=value.get("email")
        domain_name=email.split('@')[-1]

        if(domain_name not in valid_domain):
            raise ValueError("not a valid domain ")
        return value
    
    @field_validator("name")
    @classmethod

    def transform(cls,value):
        return value.upper()
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

def insert_patient_data(P:patient):
    print(P.name)
    print(P.age)
    print("inserted successfully")
    print(P.weight)
    print('BMI',P.bmi)
    print(P.married)

data={  'name':'Arju',
        'age':67,
        'github_url': 'https://github.com/arju',
        'weight':82.2,
        'height':1.75, 
        'married':True,
        'allergies':['dryfruit_allergy','bf_allergies'],
        'contact_details':{'email':'taniya.ch595@hdfc.com','phone':'7854961524','emergency':'544444'}}

patient1=patient(**data)

insert_patient_data(patient1)

temp = patient1.model_dump_json(include=['name','age'])
print(temp)
print(type(temp))