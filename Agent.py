import uuid
# Represents the insurance agent
class Agent:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.customers = []
        self.claims = []
        self.cid_list=[]

    def addCustomer(self, customer):
        if type(customer) == list:
            for c in customer:
                self.customers.append(c)
        else:
            self.customers.append(customer)

    # convert object o JSON
    def serialize(self):
        for c in self.customers:
            self.cid_list.append(c.ID)
        return {
            'id': self.ID,
            'name': self.name, 
            'address': self.address,
            'customers': self.cid_list
        }