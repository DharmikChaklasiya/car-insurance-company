from flask import Flask, request, jsonify
from InsuranceCompany import *
from Customer import *
from Agent import *
from Claim import *
from Payment import *

app = Flask(__name__)

# Root object for the insurance company
company = InsuranceCompany ("Be-Safe Insurance Company")

#Add a new customer (parameters: name, address).
@app.route("/customer", methods=["POST"])
def addCustomer():
    # parameters are passed in the body of the request
    cid = company.addCustomer(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new customer with ID {cid}")

#Return the details of a customer of the given customer_id.
@app.route("/customer/<customer_id>", methods=["GET"])
def customerInfo(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        return jsonify(c.serialize())
    return jsonify(
            success = False, 
            message = "Customer not found")

#Add a new car (parameters: model, numberplate, mototr_power).
@app.route("/customer/<customer_id>/car", methods=["POST"])
def addCar(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        car = Car(request.args.get('model_name'), request.args.get('number_plate'), request.args.get('motor_power'), request.args.get('year'))
        c.addCar (car)
        return jsonify(
                success=True,
                message="Customer is found")
    else:
        return jsonify(
            success=False,
            message="Customer not found")

#Delete the customer with the given customer_id.
@app.route("/customer/<customer_id>", methods=["DELETE"])
def deleteCustomer(customer_id):
    result = company.deleteCustomer(customer_id)
    if(result): 
        message = f"Customer with id{customer_id} was deleted"
    else: 
        message = "Customer not found"
    return jsonify(
            success = result, 
            message = message)

#Return a list of all customers.
@app.route("/customers", methods=["GET"])
def allCustomers():
    return jsonify(customers=[h.serialize() for h in company.getCustomers()])

#Add a new insurance agent (parameters: name, address).
@app.route("/agent", methods=["POST"])
def addAgent():
    # parameters are passed in the body of the request
    aid = company.addAgent(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new agent with ID {aid}")

#Return the details of an agent of the given agent_id.
@app.route("/agent/<agent_id>", methods=["GET"])
def agentInfo(agent_id):
    a = company.getAgentById(agent_id)
    if(a!=None):
        return jsonify(a.serialize())
    return jsonify(
            success = False,
            message = "Agent not found")

#Assign a new customer with the provided customer_id to the agent with agent_id.
@app.route("/agent/<agent_id>/<customer_id>", methods=["POST"])
def addCustomerToAgent(agent_id, customer_id):
    c = company.getCustomerById(customer_id)
    a = company.getAgentById(agent_id)
    if c != None and a != None:
        assigned_agent = company.getAssignedAgent(customer_id)
        if (assigned_agent != None):
            return jsonify(
                success=False,
                message=f"A customer with ID {customer_id} is already assigned to other agent.")
        a.addCustomer(c)
        return jsonify(
            success=True,
            message=f"A customer with ID {customer_id} is assigned to the agent with ID {agent_id}.")
    return jsonify(
        success=False,
        message=f"Customer or agent was not found")

#Delete the agent with the given agent_id.
#If the agent has customers, move the customers to other agent first.
@app.route("/agent/<agent_id>", methods=["DELETE"])
def deleteAgent(agent_id):
    agent_list = company.getAgents()
    a = company.getAgentById(agent_id)
    if len(agent_list) > 1:
        i=0
        while agent_list[i]==a:
            i+=1
        agent_list[i].addCustomer(a.customers)
    result = company.deleteAgent(agent_id)
    if(result):
        message = f"Agent with id{agent_id} was deleted"
    else:
        message = "Agent not found"
    return jsonify(
            success = result,
            message = message)

#Return a list of all agents.
@app.route("/agents", methods=["GET"])
def allAgents():
    return jsonify(agents=[h.serialize() for h in company.getAgents()])


# Add a new insurance claim (parameters: date, incident_description, claim_amount).
@app.route("/claims/<customer_id>/file", methods=["POST"])
def addClaim(customer_id):
    c = company.getCustomerById(customer_id)
    if (c != None):
        claim = Claim(c, request.args.get('date'), request.args.get('incident_description'), request.args.get('claim_amount'))
        claim_id = company.addClaim(claim)
        if (claim_id != None):
            return jsonify(f"New claim added with ID {claim_id}")

    return jsonify(
        success=False,
        message="Customer not found")

#Return details about the claim with the given claim_id.
@app.route("/claims/<claim_id>", methods=["GET"])
def claimInfo(claim_id):
    claim = company.getClaimById(claim_id)
    if(claim!=None):
        return jsonify(claim.serialize())
    return jsonify(
            success = False,
            message = "Claim not found")

#Change the status of a claim to REJECTED, PARTLY COVERED or FULLY COVERED. Parameters: approved_amount.
@app.route("/claims/<claim_id>/status", methods=["PUT"])
def changeClaimStatus(claim_id):
    if request.args.get('approved_amount') in ['REJECTED' ,'PARTLY COVERED' , 'FULLY COVERED']:
        claim = company.getClaimById(claim_id)
    if(claim!=None):
        newstatus = claim.changeStatus(request.args.get('approved_amount'))
        if(newstatus!=None):
            return jsonify(f"status of Claim with ID {claim_id} is updated to {newstatus}")
        return jsonify(
            success = False,
            message = "Status could not be changed")
    return jsonify(
            success = False,
            message = "Claim could not found")

#Return a list of all claims.
@app.route("/claims", methods=["GET"])
def allClaims():
    return jsonify(claims=[c.serialize() for c in company.claims])


#Add a new payment received from a customer. (parameters: date, customer_id, amount_received).
@app.route("/payment/in/", methods=["POST"])
def addPaymentIn():
    c = company.getCustomerById(request.args.get('customer_id'))
    if (c != None):
        paymentIn = PaymentIn(request.args.get('date'), request.args.get('customer_id'),
                              request.args.get('amount_received'))
        result = company.addPayment(paymentIn)
        if (result != None):
            return jsonify(
                success=True,
                message="an incoming payment added successfully")

    return jsonify(
        success=False,
        message="An incoming payment could not be added.")

#Add a new payment transferred to an agent. (parameters: date, agent_id, amount_sent).
@app.route("/payment/out/", methods=["POST"])
def addPaymentOut():
    a = company.getAgentById(request.args.get('agent_id'))
    if (a != None):
        paymentOut = PaymentOut(request.args.get('date'), request.args.get('agent_id'), request.args.get('amount_sent'))
        result = company.addPayment(paymentOut)
        if (result != None):
            return jsonify(
                success=True,
                message="an outgoing payment added successfully")
    return jsonify(
        success=False,
        message="An outgoing payment could not be added.")

#Return a list of all incoming and outgoing payments.
@app.route("/payments/", methods=["GET"])
def allPayments():
    return jsonify(payments=[h.serialize() for h in company.getPayments()])

# Return a list of all claims, grouped by responsible agents
@app.route("/stats/claims", methods=["GET"])
def allClaimsGroupedByAgents():
    result = company.claimsbyagent()
    if (result!=None):
        return jsonify(Claims=[result])
    return jsonify(
            success = False,
            message = "not available")

#Return a list of all revenues, grouped by responsible agents
@app.route("/stats/revenues", methods=["GET"])
def allRevenuesGroupedByAgents():
    result = company.RevenuesFromAgents()
    if (result != None):
        return jsonify(Revenues=[result])
    return jsonify(
        success=False,
        message="not available")

#Return a sorted list of agents based on their performance.
#Be creative and come up with a calculation scheme as performance indicator.
@app.route("/stats/agents", methods=["GET"])
def allAgentsSortedByPerformance():
    result = company.getSortedAgents()
    if (result!=None):
        return jsonify(agent_performance=[result])
    return jsonify(
            success = False,
            message = "A list of the best agents cannot be displayed")


###DO NOT CHANGE CODE BELOW THIS LINE ##############################
@app.route("/")
def index():
    return jsonify(
            success = True, 
            message = "Your server is running! Welcome to the Insurance Company API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)
