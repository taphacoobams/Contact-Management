from fastapi import FastAPI

app = FastAPI(
    title = "Contact Management"
)

# Définissez vos routes ici
@app.get("/")
def read_root():
    return {"message": "Bienvenue dans votre gestionnaire de contacts"}

@app.get("/contacts/")
def get_contacts():
    # Logique pour récupérer la liste des contacts
    pass

@app.post("/contacts/")
def create_contact():
    # Logique pour créer un nouveau contact
    pass

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):
    # Logique pour récupérer un contact par ID
    pass

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int):
    # Logique pour mettre à jour un contact
    pass

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    # Logique pour supprimer un contact
    pass
