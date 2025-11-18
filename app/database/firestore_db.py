from google.cloud import firestore
from app.models.data_models import CustomerProfile
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firestore Client
# When running on Google Cloud (Cloud Run, Cloud Shell),
# the client automatically finds the project's credentials.

# --- NEW FIX ---
# We will explicitly tell the client what project to use.
PROJECT_ID = "credflow-478510"
# --- END NEW FIX ---

try:
    db = firestore.Client(project=PROJECT_ID) # <-- UPDATED THIS LINE
    logger.info(f"Firestore client initialized successfully for project: {PROJECT_ID}")
except Exception as e:
    logger.error(f"Failed to initialize Firestore client: {e}")
    db = None

CUSTOMER_COLLECTION = "crediflow_customers"

def get_customer_by_phone(phone_number: str) -> Optional[CustomerProfile]:
    """
    Fetches a customer's profile from Firestore using their phone number.
    The phone number is used as the document ID.
    """
    if not db:
        logger.error("Firestore client not available.")
        return None
        
    try:
        doc_ref = db.collection(CUSTOMER_COLLECTION).document(phone_number)
        doc = doc_ref.get()

        if doc.exists:
            logger.info(f"Found customer: {phone_number}")
            return CustomerProfile(**doc.to_dict())
        else:
            logger.warning(f"Customer not found: {phone_number}")
            return None
    except Exception as e:
        logger.error(f"Error fetching customer {phone_number}: {e}")
        return None

def seed_database():
    """
    Adds the 10 synthetic customer profiles to Firestore.
    This is a one-time setup function.
    """
    if not db:
        logger.error("Firestore client not available. Cannot seed database.")
        return

    logger.info("Seeding database with synthetic customer data...")
    
    # Our 10 sample profiles
    synthetic_customers = [
        # 1. Ideal Profile (Instant Sanction)
        {"cust_id": "C1001", "full_name": "Rohan Sharma", "phone_number": "9876543210", "kyc_verified": True, "annual_income": 1200000, "existing_emis": 10000, "bureau_score": 780, "pre_approved_limit": 500000},
        # 2. High-Risk Profile (Instant Rejection)
        {"cust_id": "C1002", "full_name": "Priya Singh", "phone_number": "9876543211", "kyc_verified": True, "annual_income": 600000, "existing_emis": 15000, "bureau_score": 620, "pre_approved_limit": 0},
        # 3. Borderline Profile (Needs Review - High EMIs)
        {"cust_id": "C1003", "full_name": "Amit Kumar", "phone_number": "9876543212", "kyc_verified": True, "annual_income": 1000000, "existing_emis": 45000, "bureau_score": 710, "pre_approved_limit": 100000},
        # 4. KYC Not Verified (Blocker)
        {"cust_id": "C1004", "full_name": "Sunita Devi", "phone_number": "9876543213", "kyc_verified": False, "annual_income": 800000, "existing_emis": 5000, "bureau_score": 790, "pre_approved_limit": 200000},
        # 5. High Income, No Credit History (Needs Review)
        {"cust_id": "C1005", "full_name": "Vikram Rathore", "phone_number": "9876543214", "kyc_verified": True, "annual_income": 2500000, "existing_emis": 0, "bureau_score": 0, "pre_approved_limit": 0}, # 0 score = new to credit
        # 6. Low Income (Rejection)
        {"cust_id": "C1006", "full_name": "Meena Kumari", "phone_number": "9876543215", "kyc_verified": True, "annual_income": 300000, "existing_emis": 1000, "bureau_score": 740, "pre_approved_limit": 0},
        # 7. Good All-Rounder
        {"cust_id": "C1007", "full_name": "David D'souza", "phone_number": "9876543216", "kyc_verified": True, "annual_income": 900000, "existing_emis": 8000, "bureau_score": 760, "pre_approved_limit": 150000},
        # 8. High Earner, High Debt (Borderline)
        {"cust_id": "C1008", "full_name": "Ananya Reddy", "phone_number": "9876543217", "kyc_verified": True, "annual_income": 3000000, "existing_emis": 120000, "bureau_score": 720, "pre_approved_limit": 500000},
        # 9. Freelancer, Lumpy Income (Needs Review)
        {"cust_id": "C1009", "full_name": "Siddharth Jain", "phone_number": "9876543218", "kyc_verified": True, "annual_income": 1500000, "existing_emis": 20000, "bureau_score": 750, "pre_approved_limit": 0},
        # 10. Pre-Approved & Verified (Fast Path)
        {"cust_id": "C1010", "full_name": "Fatima Sheikh", "phone_number": "9876543219", "kyc_verified": True, "annual_income": 1800000, "existing_emis": 15000, "bureau_score": 810, "pre_approved_limit": 800000},
    ]

    batch = db.batch()
    count = 0
    for customer_data in synthetic_customers:
        # Use phone_number as the unique Document ID
        doc_ref = db.collection(CUSTOMER_COLLECTION).document(customer_data["phone_number"])
        # Validate with Pydantic model before sending
        profile = CustomerProfile(**customer_data)
        batch.set(doc_ref, profile.model_dump()) # <-- CHANGED FROM .dict()
        count += 1
        
    batch.commit()
    logger.info(f"Successfully seeded {count} customers in collection '{CUSTOMER_COLLECTION}'.")

if __name__ == "__main__":
    # This allows you to run `python app/database/firestore_db.py` 
    # from the project root to seed the database.
    seed_database()