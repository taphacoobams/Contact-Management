from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

#Routers
import routers.router_contacts, routers.router_auth

app = FastAPI(
    title = "Contact Management",
    description=api_description,
    openapi_tags=tags_metadata
)

app.include_router(routers.router_contacts.router)
app.include_router(routers.router_auth.router)
