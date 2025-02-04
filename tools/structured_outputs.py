from pydantic import BaseModel, Field

class EmailResponse(BaseModel):
    subject: str = Field(description="An engaging subject line to encourage the lead to open the email.")
    email: str = Field(description="The personalized email content tailored to the lead’s profile and company information.")