# PRAVAH LIVE PRODUCTION DEMO

## LIVE URL
http://pravah.blackholeinfiverse.com *(DNS pending)*
Fallback: http://54.156.236.10

---

## STREAM ENDPOINT
curl -H "Host: pravah.blackholeinfiverse.com" \
-N http://54.156.236.10/signals/stream

---

## REAL TRACE PROOF

TRACE:
544e1170-288e-4467-984e-3816fa074f13

OUTPUT:
{
  "trace_id": "544e1170-288e-4467-984e-3816fa074f13",
  "signals": [
    {"signal_type": "execution_completed", "service": "web1-blue"}
  ],
  "correlation": {
    "user_events": [
      {"event_type": "session_start"},
      {"event_type": "user_login"},
      {"event_type": "page_view"},
      {"event_type": "interaction_click"},
      {"event_type": "decision_made"},
      {"event_type": "execution_done"}
    ]
  },
  "causal_chain": ["execution"]
}

---

## FAILURE PROOF

TRACE:
94ec5f75-8067-4eb3-aa9e-0fd7ec090616

OUTPUT:
{
  "trace_id": "94ec5f75-8067-4eb3-aa9e-0fd7ec090616",
  "signals": [
    {"signal_type": "execution_failed", "service": "invalid-service"}
  ]
}

---

## SECURITY PROOF

Direct call blocked:

POST /execute-action → {"error":"unauthorized"}

---

## CONCURRENCY PROOF

5 parallel traces executed:
test1 → 2b71499d...
test2 → d111df3a...
test3 → c38b2d94...
test4 → 94dece61...
test5 → 9f5c7b43...

All appeared independently in stream.

---

## EXECUTION PROOF

kubectl get pods -n prod -w

web1-blue-OLD → Terminating  
web1-blue-NEW → Running  

---

## FINAL FLOW

Core/Web → Monitor → Sarathi → Executer → Monitor → Stream

✔ trace continuity  
✔ sarathi enforced  
✔ real infra execution  
✔ live streaming  

---

## STATUS

System is fully runnable, observable, and reproducible.