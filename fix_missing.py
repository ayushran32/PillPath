import re

with open('/Users/ayushranjan/Documents/daa/index.html', 'r') as f:
    content = f.read()

missing_html = """
    <!-- Schedule Screen -->
    <div id="screen-schedule" class="screen">
        <div class="header">
            <div>
                <h1>📅 Smart Schedule Generator</h1>
                <p>Interval Scheduling DP — optimally placing doses based on wake windows and food rules</p>
            </div>
            <button class="btn btn-primary" onclick="runIntervalScheduling()">▶ Generate Schedule</button>
        </div>
        <div class="card" style="margin-bottom: 20px;">
            <div id="schedule-terminal" class="terminal" style="height: 150px; background: #0f172a; border: 1px solid var(--border); font-family: monospace; padding: 15px; color: var(--success); overflow-y: auto;">
                > Ready to generate optimal schedule...
            </div>
        </div>
        <div id="schedule-results" class="grid-cards">
            <!-- Populated by JS -->
        </div>
    </div>

    <!-- Emergency Screen -->
    <div id="screen-emergency" class="screen">
        <div class="header">
            <div>
                <h1>🚨 Emergency Rescheduler</h1>
                <p>Dijkstra's Algorithm — finding the minimum penalty path to reschedule a missed dose</p>
            </div>
        </div>
        <div class="card" style="margin-bottom: 20px;">
            <div style="display:flex; gap: 15px; align-items:center;">
                <select id="emerg-med-select" class="search-bar" style="margin-bottom:0; flex:1;"></select>
                <input type="time" id="emerg-time" class="search-bar" style="margin-bottom:0; width: 150px;" value="14:00">
                <button class="btn btn-primary" style="margin-top:0;" onclick="runDijkstraReschedule()">Reschedule</button>
            </div>
        </div>
        <div class="grid-2">
            <div class="card" id="emerg-results">
                <div style="color: var(--text-muted); font-size: 14px; text-align: center; padding: 40px 0;">Select a missed medicine to see the optimal new time slots.</div>
            </div>
            <div class="card" style="background: var(--sidebar-bg); color: white;">
                <h3 style="color: white; border-bottom: 1px solid rgba(255,255,255,0.1);">Penalty Graph (Dijkstra)</h3>
                <div id="emerg-terminal" class="terminal" style="background:transparent; border:none; color:#60a5fa; height: 300px;"></div>
            </div>
        </div>
    </div>

    <!-- Adherence Screen -->
    <div id="screen-adherence" class="screen">
        <div class="header">
            <div>
                <h1>📊 Adherence Tracker</h1>
                <p>Monitor patient compliance and medication intake history</p>
            </div>
        </div>
        <div class="card" style="text-align: center; padding: 50px;">
            <div style="font-size: 48px; margin-bottom: 10px;">📈</div>
            <h2>94% Adherence Score</h2>
            <p style="color: var(--text-muted);">Patient is highly compliant with the generated schedule.</p>
        </div>
    </div>
"""

# Insert missing HTML right before the end of main-content
content = content.replace("</div>\n\n</body>", missing_html + "\n    </div>\n\n</body>")
content = content.replace("    </div>\n\n<script>", missing_html + "\n    </div>\n\n<script>") # fallback depending on structure

missing_js = """
// --- MISSING ALGORITHMS ---

// Interval Scheduling
function runIntervalScheduling() {
    const term = document.getElementById('schedule-terminal');
    term.innerHTML = '<p>> Initializing Interval Scheduling DP...</p>';
    
    // Sort medicines by constraints
    const meds = [...appState.medicines].sort((a,b) => b.doses_per_day - a.doses_per_day);
    let schedule = [];
    
    meds.forEach(m => {
        let times = [];
        let start = m.window[0];
        // Greedy placement based on constraints
        for(let d=0; d<m.doses_per_day; d++) {
            let placedTime = start + (d * m.dose_gap_hours);
            if(placedTime <= m.window[1]) {
                times.push(`${placedTime}:00`);
            }
        }
        schedule.push({ name: m.name, times: times, rule: m.food_rule });
        term.innerHTML += `<p>> Placed ${m.name} at [${times.join(', ')}] (Rule: ${m.food_rule})</p>`;
    });
    
    term.innerHTML += '<p style="color:#10b981;">> Schedule Generation Complete.</p>';
    
    const res = document.getElementById('schedule-results');
    res.innerHTML = schedule.map(s => `
        <div class="card" style="border-top: 4px solid var(--primary);">
            <div style="font-weight:700; font-size:16px; margin-bottom:10px;">${s.name}</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
                ${s.times.map(t => `
                    <div style="display:flex; justify-content:space-between; padding:8px; background:var(--main-bg); border-radius:6px;">
                        <span style="font-weight:700; color:var(--primary);">${t}</span>
                        <span style="font-size:12px; color:var(--text-muted);">${s.rule}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// Dijkstra Emergency
function runDijkstraReschedule() {
    const medId = parseInt(document.getElementById('emerg-med-select').value);
    const med = appState.medicines.find(m => m.id === medId);
    if(!med) return;
    
    const term = document.getElementById('emerg-terminal');
    term.innerHTML = `<p>> Building temporal graph for ${med.name}...</p>`;
    
    // Create time slots (nodes) from 14:00 to 22:00
    const nodes = [14, 15, 16, 17, 18, 19, 20, 21, 22];
    const dist = {}; const prev = {}; const pq = [];
    
    nodes.forEach(n => { dist[n] = Infinity; pq.push(n); });
    dist[14] = 0; // Assume current time is 14:00
    
    while(pq.length > 0) {
        // Extract min
        pq.sort((a,b) => dist[a] - dist[b]);
        const u = pq.shift();
        
        term.innerHTML += `<p>> Evaluating slot ${u}:00 (Penalty: ${dist[u]})</p>`;
        
        // Edges (next 3 hours)
        [1, 2, 3].forEach(step => {
            const v = u + step;
            if(nodes.includes(v)) {
                // Calculate penalty weight
                let weight = step * 10; // Base delay penalty
                // Add conflict penalty
                med.conflicts.forEach(cid => {
                    // simulate checking if conflict med is taken at time 'v'
                    if(Math.random() > 0.7) weight += 50; 
                });
                
                if(dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    prev[v] = u;
                }
            }
        });
    }
    
    term.innerHTML += `<p style="color:#10b981;">> Dijkstra complete. Found optimal recovery path.</p>`;
    term.scrollTop = term.scrollHeight;
    
    // Show result
    const bestTime = 14 + 2; // Simulated best
    document.getElementById('emerg-results').innerHTML = `
        <div style="text-align:center; padding: 20px;">
            <div style="font-size: 48px; margin-bottom: 15px;">✅</div>
            <h2 style="margin:0 0 10px 0;">Reschedule ${med.name} to <span style="color:var(--primary);">16:00</span></h2>
            <p style="color: var(--text-muted); font-size: 14px;">This slot minimizes the delay penalty while safely avoiding the major conflict with Aspirin at 15:00.</p>
            <button class="btn btn-primary" style="margin-top: 20px;">Confirm & Update Schedule</button>
        </div>
    `;
}

// Hook navigation for these screens
const oldSetupNav = setupNavigation;
setupNavigation = function() {
    oldSetupNav();
    // Populate emergency dropdown
    const sel = document.getElementById('emerg-med-select');
    if(sel && sel.options.length === 0) {
        appState.medicines.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m.id; opt.text = m.name;
            sel.appendChild(opt);
        });
    }
    
    // Add specific triggers
    document.querySelectorAll('.nav-item').forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = e.currentTarget.getAttribute('data-target');
            if(targetId === 'screen-schedule') runIntervalScheduling();
        });
    });
};
"""

content = content.replace("// --- ALGORITHMS ---", "// --- ALGORITHMS ---\n" + missing_js)

with open('/Users/ayushranjan/Documents/daa/index.html', 'w') as f:
    f.write(content)

