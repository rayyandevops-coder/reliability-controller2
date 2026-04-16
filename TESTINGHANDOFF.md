# TESTING HANDOFF — PRAVAH

---

## 🔹 Run System

kubectl apply -f k8s/

Access:
http://54.156.236.10:30004

---

## 🔹 Test Cases

---

### ✅ 1. User Activity

Steps:

* Login (rayyan, test1)
* Click multiple times

Check:

curl http://54.156.236.10:30004/user-metrics

Expected:

✔ active_users = 2
✔ total_users = 2
✔ activity counts updated

---

### ✅ 2. Summary

curl http://54.156.236.10:30004/summary

Expected:

✔ engagement_level = high
✔ drop_off_area = low

---

### ✅ 3. Streaming (CRITICAL)

curl http://54.156.236.10:30004/signals/stream

Expected:

✔ continuous stream
✔ includes:

* pod_crash
* execution_failure
* deployment_success

✔ includes correlation

---

### ❌ Failure Cases

| Test           | Expected |
| -------------- | -------- |
| empty user_id  | rejected |
| missing fields | error    |
| invalid metric | rejected |

---

## 🔹 PASS Criteria

✔ real user data present
✔ correct summary
✔ valid signals
✔ correlation working
✔ streaming active

---

## 🔹 FAIL Criteria

❌ zero users
❌ static summary
❌ missing signals
❌ no correlation

---

## 🎯 Goal

System must be:

deterministic
validated
real-data driven
traceable
