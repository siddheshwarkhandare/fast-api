
from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

import json

app = FastAPI()# object of the fastapi this is import for any project

class patiant(BaseModel):
    
    id :Annotated[str, Field(..., description=' ID of patiant ',examples=['P001'])]
    name:Annotated[str, Field(..., description= 'Name of the patiant', examples=['ramesh'])]
    city:Annotated[str, Field(..., description= 'where is pataint living', examples=['pune'])]
    age:Annotated[int, Field(..., gt=0, lt=120,description= 'AGE of patiant')]
    gender:Annotated[Literal['MALE','FEMALE','other'] , Field(..., description= 'Gender of the patiant')]
    height: Annotated[float,Field(..., gt=0, description= "height of the patiant in meter")]
    weight:Annotated[float,Field(..., gt=0, description="weigth of patiant in kg" )] 

    #it for data validation 
    # if input data is not in the right format it will through an error 

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    # it calculating the BMI of patiant


    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return'underweight'
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return"normal"
        else:
            return"obese"
     # based on the patiant BMI it is puting them in diffrant category



#CURD (creat,update,read,delete) this are import api componet
@app.get("/")# this is get request that get data from the data base it also provide loction to the url 
             #When someone sends an HTTP GET request to the / (root) URL, run the function below.

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f: 
      json.dump(data,f)


def read_root():
    return{"Hello":"patian magement api"}

@app.get("/about")

def about():
    return{"Massege":"fully functional mangement api"}


@app.get('/view')
def view():
    data=load_data()

    return data


@app.get('/patients/{patients_id}')
def view_patiant(patients_id: str=Path(..., description='id of patiant in the DB', example=["P001"])):
    data=load_data()

    if patients_id in data:
        return data[patients_id]
    raise HTTPException(status_code=404,detail="patiant not found")
    # it is showing if patient is in the DB it will show patient or raise an error

@app.get('/sort') 
# this method allow user to sort the patient on the basis of hight,weigth,bmi

def sort_patiants(sort_by :str =Query (...,description='sorting on the basis of hight weight bmi'), order:str=Query('asc',description="sorting in the ascending order ")):
    
    valid_filed=['hieght','weight','bmi']

    if sort_by not in valid_filed:
        raise HTTPException(status_code=400,detail="invalid file select by {valid_filed}") 
    # 400 mean bad request
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="invalid order selected between ascending and desending ") 
    
    data=load_data()

    sort_order= True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data 

# now creating post method 

@app.post("/create")
def cteate_patient(patiant: patiant):# data comming form request body that is going thorugh the pydantic model for data validation
    
    # loaing eaxsting data 
    data=load_data()

    # check if paitent in the dataset
    if patiant.id in data:
        raise HTTPException(status_code=400,detail="patian is already exists")
    
    # adsing new patiant in DB
    data[patiant.id]=patiant.model_dump(exclude=['id'])
    #model_dump convert pydantic model into dictionry

    # now saving the data in the DB
    save_data(data)

    # now giving respose that patient has been created 
    return JSONResponse(status_code=201,content={'massage':'paitant created successfully'})