# car-insurance-company

This programming task is about implementing a web API, so that the same software can be used by
different insurance companies to build their own applications using the provided API. At the
moment, we do not care about the front-end application, which could be any browser or a mobile
app. And we also don’t care about a database that stores the information. In this exercise, we
deal with the API implementation only. You may use a REST client like Postman to quickly see the
results of the API call.

The API consists of the following functionality:
 Management of customers
    o Add/remove customers to/from the system. Each customer has a customer-id, name, address
      and at least one car associated with the customer number.
    o Add/remove cars to/from customers. Each car has at least the model name, number plate,
      motor power and the year it was manufactured in.
    o Each customer has an insurance agent, who is responsible for him/her.
 Management of insurance agents
    o Add/remove agents to/from the system. Each agent has an agent-id, name, address.
    o When an agent is removed, transfer all customers in his/her supervision to another
      agent first.
 Management of insurance claims
    o Customers can file up insurance claims. Such claims are first reviewed by the                 responsible agent and then passed on to the insurance company. Each claim is assigned a       unique claim-id.
    o Claims are either rejected, partly covered, or fully covered by the insurance policy.
 Management of financials
    o The system keeps track of the payments made by the customer.
    o Based on the number of customers, and their claims, the agents are paid a monthly             revenue.
 Management of general statistics
    o Display total revenue and profits of the insurance company
    o Display claim statistics per customer
    o Display the best agent (customers, claims, …)

The API is implemented in Python using a package called Flask, which allows you to define HTML
methods GET, POST, PUT etc. Each method returns a JSON object, which can be used by the front-end-application in adequate ways.

![image](https://user-images.githubusercontent.com/79636839/114850041-aa47cf00-9de0-11eb-9047-31a49c1f9e7f.png)

![image](https://user-images.githubusercontent.com/79636839/114850162-c64b7080-9de0-11eb-88d6-feab09b37f1a.png)
