from fastapi import APIRouter, Header, Request, Depends, Body
from fastapi.responses import RedirectResponse
import stripe
from firebase_admin import auth
from database.firebase import db
from routers.router_auth import get_current_user
from dotenv import dotenv_values

router = APIRouter(
    tags=["Stripe"],
    prefix='/stripe'
)

stripe.api_key= 'sk_test_51OA7iPCnvtvx8aFI4QrKivrvcsffMruSkSQb2odifm1mMCNPpaJL5sqcWpY7kOFIGxkiUq54aWMgfJqMSV03jGT800pWyZZV5k'

YOUR_DOMAIN = 'http://localhost'

@router.get('/checkout')
async def stripe_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # PRICE ID du produit que vous vouler vendre
                    'price':'price_1OA8tlCnvtvx8aFI5WwXYSod',
                    'quantity' : 1,
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url=YOUR_DOMAIN + '/stripe/success', 
            cancel_url=YOUR_DOMAIN + '/stripe/cancel',
        )
        # return checkout_session
        response = RedirectResponse(url=checkout_session['url'])
        return response
    except Exception as e:
        return str(e)
    
@router.post('/webhook')
async def webhook_received(request:Request, stripe_signature: str = Header (None)):
    webhook_secret = "whsec_c17400b9ae2294360f3e7e70895830fc54b01140bf5b1405c3f4954be5c05c7c"
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload = data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        event_data =event['data']
    except Exception as e:
        return  {"error":str(e)}
    
    event_type = event['type']
    if event_type == 'checkout.session.completed':
        print('checkout session completed')
    elif event_type == 'invoice.paid':
        print('invoice paid')
        cust_email = event_data['object']['customer_email'] # email de notre customer
        fireBase_user = auth.get_user_by_email(cust_email) # Identifiant firebase correspondant (uid)
        cust_id =event_data['object']['customer'] # Stripe ref du customer
        item_id= event_data['object']['lines']['data'][0]['subscription_item']
        db.child("users").child(fireBase_user.uid).child("stripe").set({"item_id":item_id, "cust_id":cust_id}) # écriture dans la DB firebase      

    elif event_type == 'invoice.payment_failed':
        print('invoice payment failed')
    else:
        print(f'unhandled event: {event_type}')

    return {"status": "success"}

@router.get('/usage')
async def stripe_usage(userData: int = Depends(get_current_user)):
    fireBase_user = auth.get_user(userData['uid']) # Identifiant firebase correspondant (uid)
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    cust_id =stripe_data['cust_id']
    return stripe.Invoice.upcoming(customer=cust_id)

def increment_stripe(userId:str):
    fireBase_user = auth.get_user(userId) # Identifiant firebase correspondant (uid)
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    print(stripe_data.values())
    item_id =stripe_data['item_id']
    stripe.SubscriptionItem.create_usage_record(item_id, quantity=1)
    return