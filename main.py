
from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()# object of the fastapi this is import for any project

#CURD (creat,update,read,delete) this are import api componet
@app.get("/")# this is get request that get data from the data base it also provide loction to the url 
             #When someone sends an HTTP GET request to the / (root) URL, run the function below.

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def read_root():
    return{"hello":"patian magement api"}

@app.get("/about")

def about():
    return{"massege":"fully functional mangement api"}


@app.get('/view')
def view():
    data=load_data()

    return data


@app.get('/patients/{patients_id}')
def view_patiant(patients_id: str=Path(..., description='id of patiant in the DB',example="P001")):
    data=load_data()

    if patients_id in data:
        return data[patients_id]
    raise HTTPException(status_code=404,detail="patiant not found")

@app.get('/sort')
def sort_patiants(sort_by :str =Query (...,description='sorting on the basis of hight weight bmi'), order:str=Query('asc',description="sorting in the ascending order ")):
    
    valid_filed=['hieght','weight','bmi']

    if sort_by not in valid_filed:
        raise HTTPException(status_code=400,detail="invalid file select by {valid_filed}") 
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="invalid order selected between ascending and desending ") 
    
    data=load_data()

    sort_order= True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data 