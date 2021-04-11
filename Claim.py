from Customer import *

#represents the claima
class Claim:
    def __init__(self, customer, date, incident_description, claim_amount):
        self.ID = str(uuid.uuid1())
        self.customer = customer
        self.date = date
        self.incident_description = incident_description
        self.claim_amount = claim_amount
        self.approved_amount = None

    def changeStatus(self, status):
        self.approved_amount = status
        return True

    def serialize(self):
        return {
            'claim_id': self.ID,
            'Customer-Sender': self.customer.ID,
            'date': self.date,
            'incident_description': self.incident_description,
            'claim_amount': self.claim_amount,
            'approved_amount': self.approved_amount
        }