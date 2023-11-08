from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from classes.schema_dto import Contact, ContactNoID
from database.firebase import db
from routers.router_auth import get_current_user

router = APIRouter(
    tags=["Contacts"],
    prefix='/contacts' 
)

contacts = [
    Contact(id="1", first_name="Amadou", last_name="Ba", email="amba@gmail.com", phone_number="0612345678", adress="Paris"), 
    Contact(id="2", first_name="Bastien", last_name="Dupont", email="dupontbastien@gmail.com", phone_number="0612349178", adress="Lyon"),
    Contact(id="3", first_name="Charles", last_name="Dubois", email="charlesdub@gmail.com", phone_number="0646545678", adress="Lille")
]

@router.get('/', response_model=List[Contact])
async def get_contact(userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('contact').get(userData['idToken']).val()
    resultArray = [value for value in fireBaseobject.values()]
    return resultArray

@router.post('/', response_model=Contact, status_code=201)
async def create_contact(givenName: ContactNoID, userData: int = Depends(get_current_user)):
    generatedId = uuid.uuid4()
    newContact = Contact(id=str(generatedId), name=givenName)
    contacts.append(newContact)
    db.child("users").child(userData['uid']).child("contact").child(str(generatedId)).set(newContact.model_dump())
    return newContact

@router.get('/{contact_id}', response_model=Contact)
async def get_contact_by_ID(contact_id: str, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('contact').child(contact_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        return fireBaseobject
    raise HTTPException(status_code=404, detail="Contact not found")

@router.patch('/{contact_id}', status_code=204)
async def modify_contact_name(contact_id: str, modifiedContact: ContactNoID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('contacts').child(contact_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        updatedContact = Contact(id=contact_id, **modifiedContact.model_dump())
        return db.child("users").child(userData['uid']).child('contacts').child(contact_id).update(updatedContact.model_dump(), userData['idToken'] )
    raise HTTPException(status_code= 404, detail="Contact not found")

@router.delete('/{contact_id}', status_code=204)
async def delete_contact(contact_id: str, userData: int = Depends(get_current_user)):
    try:
        fireBaseobject = db.child("users").child(userData['uid']).child('contacts').child(contact_id).get(userData['idToken']).val()
    except:
        raise HTTPException(
            status_code=403, detail="Accès interdit"
        )
    if fireBaseobject is not None:
        return db.child("users").child(userData['uid']).child('contacts').child(contact_id).remove(userData['idToken'])
    raise HTTPException(status_code= 404, detail="Contact not found")
