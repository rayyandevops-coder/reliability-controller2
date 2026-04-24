# PRAVAH — FAILURE DEMO

## Test

Force failure by deleting pod:

kubectl delete pod <web1-blue-pod> -n prod

---

## Expected Behavior

✔ System remains stable  
✔ Stream continues  
✔ Failure event appears  
✔ Same trace_id maintained  

---

## Validation

✔ No crash  
✔ Trace continuity intact  
✔ Observability preserved  