# PillPath: Smart Medication Scheduling & Conflict Resolution System

## 1. Project Overview
**PillPath** is an algorithm-driven web application designed to bridge the gap between doctor prescriptions and patient adherence. Managing complex, multi-drug regimens is a significant challenge in modern healthcare. Patients often struggle to remember when to take their medicines, while doctors struggle to manually balance the therapeutic benefits of a regimen against cumulative side effects and dangerous drug-drug interactions.

PillPath solves this by applying classical computer science algorithms from **Design and Analysis of Algorithms (DAA)** to automate the scheduling, optimization, and conflict resolution of patient medication.

---

## 2. Core DAA Algorithms & Implementations

The core logic of PillPath is powered by 5 distinct algorithms, each solving a specific healthcare constraint.

### A. Graph Coloring Algorithm (Welsh-Powell)
* **Application**: Drug Interaction & Conflict Resolution.
* **How it works**: When a patient is prescribed multiple drugs, some combinations can cause severe adverse reactions. The system models the patient's prescription as an undirected graph.
    * **Nodes**: Represent the prescribed medicines.
    * **Edges**: Represent a dangerous interaction between two medicines.
* **Execution**: The Welsh-Powell algorithm sorts the medicines by their degree of conflict (number of edges). It then assigns "colors" (which represent distinct time slots) to each node. If two medicines share an edge, they are forced into different colors. This mathematically guarantees that conflicting drugs are scheduled far apart from each other.

### B. 0/1 Knapsack Problem (Dynamic Programming)
* **Application**: Prescription Optimization & Side-Effect Budgeting.
* **How it works**: Doctors must often prescribe optional supplements or secondary medications without overwhelming the patient's body.
    * **Weight**: The "Side Effect Score" of a medicine.
    * **Value**: The "Therapeutic Value" of a medicine.
    * **Capacity**: The patient's maximum tolerable side-effect limit (the "Budget").
* **Execution**: The system uses a 2D Dynamic Programming matrix to find the exact combination of optional medicines that maximizes the total therapeutic value without exceeding the patient's side-effect budget. 

### C. Interval Scheduling (Greedy Approach)
* **Application**: Daily Schedule Generation.
* **How it works**: Medicines have strict temporal constraints, such as requiring an "Empty Stomach" or needing a "12-hour gap" between doses.
* **Execution**: The greedy algorithm sorts the medicines by priority (most constrained first, e.g., drugs requiring 3 doses a day). It then iterates through the patient's "wake window" (e.g., 7:00 AM to 10:00 PM) and greedily assigns the medication to the earliest valid time slot that satisfies all food and gap constraints, ensuring no overlaps.

### D. Dijkstra's Algorithm (Shortest Path)
* **Application**: Emergency Rescheduling for Missed Doses.
* **How it works**: If a patient misses a dose, arbitrarily taking it later can inadvertently trigger a drug interaction with a different scheduled medicine. 
* **Execution**: The system treats future time slots as nodes in a graph. The algorithm calculates the "edge weights" (penalties) for moving the dose to a future slot. The weight increases based on the time delay, but it adds a massive penalty if that future slot already contains a conflicting medicine. Dijkstra's algorithm finds the "shortest path" (the lowest penalty time slot) to safely recover the missed dose.

### E. Edit Distance (Levenshtein) & Boyer-Moore
* **Application**: Medical Database Search.
* **How it works**: Medical names are notoriously difficult to spell (e.g., *Hydrochlorothiazide*, *Levetiracetam*).
* **Execution**: When a doctor searches for a medicine to add to a prescription, the system uses string-matching heuristics and Edit Distance to provide lightning-fast, typo-tolerant search results, ensuring they find the correct drug even with spelling mistakes.

---

## 3. System Features & User Roles

The system is split into two distinct, role-based interfaces sharing a centralized database.

### 👨‍⚕️ Doctor Portal
* **Clinical Overview**: Monitor patient vitals (Blood Pressure, Glucose, Weight) and adherence scores.
* **Prescription Management**: Add or remove medications from a patient's regimen.
* **Knapsack Optimizer**: Dynamically adjust the side-effect budget slider and run the DP algorithm to automatically generate the safest, most effective prescription subset.
* **Conflict Analysis**: View the dynamic Welsh-Powell graph to visually understand exactly why certain medications cannot be taken together.

### 👤 Patient Portal
* **Simplified Dashboard**: A clean, accessible view of "Today's Schedule" focusing strictly on what to take and when.
* **Adherence Tracking**: Patients can mark doses as "Taken" (✅) or "Missed" (❌), which dynamically updates their global Adherence Score for the doctor to review.
* **Emergency Rescheduler**: If a dose is missed, patients can trigger Dijkstra's algorithm to instantly receive a newly calculated, safe time slot for the missed pill.
* **Visual Cues**: Clear badging for requirements like "Empty Stomach" or "After Food".

---

## 4. Technical Stack
* **Frontend**: HTML5, Vanilla JavaScript (ES6+), Vanilla CSS3.
* **State Management**: Custom centralized `appState` controller.
* **Persistence**: Browser `localStorage` mimicking a NoSQL document database, allowing complete offline functionality and cross-session persistence.
* **Architecture**: Single Page Application (SPA) with dynamic DOM manipulation and algorithm-driven rendering.
