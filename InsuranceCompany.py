from Customer import *
from Agent import *
from Claim import *
from Payment import *


class InsuranceCompany:
    def __init__(self, name):
        self.name = name  # Name of the Insurance company
        self.customers = []  # list of customers
        self.agents = []  # list of dealers
        self.payments = []  # list of all payments
        self.claims = []  # list of all claims

    def getCustomers(self):
        return list(self.customers)

    def addCustomer(self, name, address):
        c = Customer(name, address)
        self.customers.append(c)
        return c.ID

    def getCustomerById(self, id_):
        for c in self.customers:
            if (c.ID == id_):
                return c
        return None

    def deleteCustomer(self, customer_id):
        c = self.getCustomerById(customer_id)
        self.customers.remove(c)
        return True

    def getAssignedAgent(self, customer_id):
        for a in self.agents:
            for c in a.customers:
                if (customer_id == c.ID):
                    return a
        return None

    def getAgents(self):
        return list(self.agents)

    def addAgent(self, name, address):
        a = Agent(name, address)
        self.agents.append(a)
        return a.ID

    def getAgentById(self, id_):
        for agent in self.agents:
            if (agent.ID == id_):
                return agent
        return None

    def deleteAgent(self, agent_id):
        a = self.getAgentById(agent_id)
        self.agents.remove(a)
        return True

    def addClaim(self, c):
        self.claims.append(c)
        return c.ID

    def getClaimById(self, id_):
        for claim in self.claims:
            if (claim.ID == id_):
                return claim
        return None

    def getClaims(self):
        return list(self.claims)

    # payment methods
    def addPayment(self, p):
        self.payments.append(p)
        return True

    def getPayments(self):
        return list(self.payments)

    def claimsbyagent(self):
        dict1 = {}
        for c in self.claims:
            a = self.getAssignedAgent(c.ID)
            if a.ID not in dict1:
                dict1[a.ID] = []
            dict1[a.ID].append(c.serialize())
        return dict1

    def RevenuesFromAgents(self):
        revenues = {}
        for payment in self.payments:
            if payment.inPayment == False:
                for a in self.agents:
                    if payment.agent_id == a.ID:
                        if a.ID not in dict1:
                            revenues[a.ID] = []
                        revenues[a.ID].append(payment.serialize())
        return revenues

    def getSortedAgents(self):
        allAgents = {}
        for a in self.agents:
            allAgents[a] = len(a.customers)
            for claim in self.claims:
                if claim.customer in a.customers:
                    if claim.approved_amount == 'REJECTED':
                        allAgents[a] += 1
                    elif claim.approved_amount == 'PARTLY COVERED':
                        allAgents[a] += 2
                    elif claim.approved_amount == 'FULLY COVERED':
                        allAgents[a] += 3
        sortedList = sorted(allAgents.items(), key=lambda kv: (kv[1], kv[0]))

        listSerialized = [a.serialize() for a in sortedList]
        return listSerialized
