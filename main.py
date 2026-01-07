from fastapi import FastAPI,Path,HTTPException,Query
app= FastAPI()
import json
def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {'message':'Hello World'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str= Path(...,description="Path of the Patient Id in DB",example='P001')):
    data=load_data()
    if(patient_id in data):
        return data[patient_id]
    else:
       raise HTTPException(status_code=404,detail="Patient not found ")
    

@app.get("/sort")
def sort_patient(sort_by: str=Query(...,description="sort on the basis of the height,weight and bmi"),order:str=Query('asc',description='sort in asc or desc order')):
    valid_data=['height','weight','bmi']
    if sort_by not in valid_data:
        raise HTTPException(status_code=400,detail=f'invalid field select from {valid_data}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400 ,detail='Invalid order select from asc or desc ')

    data = load_data()

    sort_order = True if order =='desc' else False

    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return data