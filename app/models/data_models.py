from pydantic import BaseModel, Field
from typing import Optional

class CustomerProfile(BaseModel):
    """
    Defines the customer data structure stored in Firestore.
    """
    cust_id: str = Field(..., description="Unique Customer ID")
    full_name: str = Field(..., description="Customer's full name")
    phone_number: str = Field(..., description="Primary phone number (used as Firestore Doc ID)")
    kyc_verified: bool = Field(default=False, description="Whether KYC is verified")
    annual_income: int = Field(..., description="Annual income in INR")
    existing_emis: int = Field(default=0, description="Total current monthly EMIs")
    bureau_score: int = Field(..., description="Credit score (e.g., CIBIL)")
    pre_approved_limit: int = Field(default=0, description="Pre-approved loan limit, if any")

class LoanRequest(BaseModel):
    """
    Defines the data model for a new loan request from the user.
    """
    phone_number: str = Field(..., description="Customer's phone number to link the request")
    requested_amount: int = Field(..., description="The loan amount the user is asking for")
    requested_tenure_months: int = Field(..., description="Loan tenure in months")

class AgentToolResponse(BaseModel):
    """
    A structured response from a worker agent tool.
    """
    status: str = Field(..., description="Status of the operation (e.g., 'success', 'error', 'needs_review')")
    message: str = Field(..., description="A human-readable message about the outcome")
    data: Optional[dict] = Field(default=None, description="Any data payload (e.g., customer details)")