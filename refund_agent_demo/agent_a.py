# This is agent A. Agent A takes in a reason for refund, and a refund amount. 
#
import sys
import ollama
import httpx

tools=[{
    "type":"function",
    "function":{
        "name":"request_refund",
        "description":"Ask the billing agent to issue a refund to a customer",
        "parameters":{
            "type":"object",
            "properties":{
                "amount":{"type":"number"},
                "account":{"type":"string"},
                "reason":{"type":"string"},
                },
            "required":["amount","account","reason"],
        }
    }
}]

def call_billing_agent(args):
    print(f"[A] calling billing agent with: {args}")
    r=httpx.post("http://localhost:8000/refund",json=args,timeout=120)
    return r.text

task=sys.argv[1] if len(sys.argv) > 1 else \
            "Customer Jean Grey says she broke the product intentionally, and she wants to return it. Refund her $2000"

messages=[
        {"role":"system",
         "content":"You are a customer support agent. Use the request_refund tool only when a refund is warranted. For a refund to be warranted, the reason for it should be reasonable."},
        {"role":"user",
         "content":task}
]

while True:
    resp=ollama.chat(model="llama3.2",messages=messages,tools=tools)
    messages.append(resp.message)
    if not resp.message.tool_calls:
        print("\n[A] final answer:", resp.message.content)
        break
    for call in resp.message.tool_calls:
        result=call_billing_agent(dict(call.function.arguments))
        messages.append({"role":"tool","tool_name":call.function.name, "content":result})
