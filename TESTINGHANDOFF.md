
---

# 📄 ✅ TESTING_HANDOFF.md (FINAL)

```md
# TESTING HANDOFF — PRAVAH SYSTEM

---

## 🔹 How to Run

1. Deploy system:

kubectl apply -f k8s/

2. Get Node IP:

kubectl get nodes -o wide

3. Access Monitor:

http://54.156.236.10:30004

---

## 🔹 Endpoints

GET /health  
GET /user-metrics  
GET /page-metrics  
GET /user-context  
GET /aggregate  
GET /summary  
GET /signals/stream  

---

## 🔹 Test Cases

---

### ✅ 1. User Flow

Steps:
- Open web1/web2
- Login
- Click button

Check:

curl /user-metrics

Expected:
✔ users count increases  
✔ activity tracked  

---

### ✅ 2. Page Tracking

curl /page-metrics

Expected:
✔ views  
✔ clicks  
✔ avg_time_spent  

---

### ✅ 3. Context Tracking

curl /user-context

Expected:
✔ device  
✔ region  
✔ source  

---

### ✅ 4. Infra Failure

kubectl delete pod web1-blue

curl /signals/stream

Expected:
✔ pod_crash  
✔ restart_count  

---

### ✅ 5. Streaming (CRITICAL)

curl /signals/stream

Expected:
✔ continuous output  
✔ includes signals + correlation  

---

### ❌ Failure Scenarios

| Test | Expected |
|-----|--------|
| empty user_id | rejected |
| invalid signal | validation error |
| wrong metric | rejected |
| duplicate signals | removed |

---

## 🔹 PASS Criteria

✔ real events captured  
✔ valid schema  
✔ correct metrics  
✔ trace continuity  
✔ correlation present  
✔ streaming working  

---

## 🔹 FAIL Criteria

❌ missing fields  
❌ wrong mapping  
❌ invalid schema  
❌ no trace  
❌ stream broken  

---

## 🎯 Final Goal

System must be:

deterministic  
structured  
validated  
traceable  
real-time  