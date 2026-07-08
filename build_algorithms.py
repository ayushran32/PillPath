import re

with open('/Users/ayushranjan/Documents/daa/index.html', 'r') as f:
    content = f.read()

algorithms_js = """
// ==========================================
// 1. TRIE (PREFIX TREE) - ADDRESS AUTOCOMPLETE
// ==========================================
class TrieNode {
    constructor() { this.children = {}; this.isEndOfWord = false; this.fullAddress = ""; }
}
class Trie {
    constructor() { this.root = new TrieNode(); }
    insert(word) {
        let node = this.root;
        const lower = word.toLowerCase();
        for (let i = 0; i < lower.length; i++) {
            const char = lower[i];
            if (!node.children[char]) node.children[char] = new TrieNode();
            node = node.children[char];
        }
        node.isEndOfWord = true;
        node.fullAddress = word;
    }
    searchPrefix(prefix) {
        let node = this.root;
        const lower = prefix.toLowerCase();
        for (let i = 0; i < lower.length; i++) {
            const char = lower[i];
            if (!node.children[char]) return [];
            node = node.children[char];
        }
        return this.collectAllWords(node, []);
    }
    collectAllWords(node, results) {
        if (node.isEndOfWord) results.push(node.fullAddress);
        for (const char in node.children) {
            this.collectAllWords(node.children[char], results);
        }
        return results;
    }
}

// Generate Mock Addresses
const addressTrie = new Trie();
const streets = ["Maple St", "Oak Ave", "Pine Ln", "Cedar Blvd", "Elm Dr", "Washington Way", "Lincoln Rd"];
for(let i=0; i<5000; i++) {
    addressTrie.insert(`${Math.floor(Math.random()*9000)+100} ${streets[Math.floor(Math.random()*streets.length)]}`);
}
addressTrie.insert("123 Main Street");
addressTrie.insert("124 Main Street");
addressTrie.insert("125 Market Ave");

document.getElementById('address-input').addEventListener('input', (e) => {
    const val = e.target.value;
    const resUl = document.getElementById('autocomplete-results');
    clearLog('trie-terminal');
    
    if(!val) { resUl.style.display = 'none'; return; }
    
    const startTime = performance.now();
    const results = addressTrie.searchPrefix(val);
    const timeTaken = performance.now() - startTime;
    
    log('trie-terminal', `Searching prefix: "${val}"`);
    log('trie-terminal', `Found ${results.length} matches in ${timeTaken.toFixed(2)}ms`, "highlight");
    
    resUl.innerHTML = '';
    if(results.length > 0) {
        resUl.style.display = 'block';
        results.slice(0, 10).forEach(r => {
            const li = document.createElement('li');
            li.className = 'autocomplete-item';
            li.innerText = r;
            li.onclick = () => { document.getElementById('address-input').value = r; resUl.style.display = 'none'; };
            resUl.appendChild(li);
        });
    } else {
        resUl.style.display = 'none';
    }
});


// ==========================================
// 2. BLOOM FILTER - SECURITY GATEWAY
// ==========================================
class BloomFilter {
    constructor(size, hashCount) {
        this.size = size;
        this.hashCount = hashCount;
        this.bitArray = new Array(size).fill(false);
    }
    
    // Simple hash functions for demo
    hash1(str) { let hash = 0; for(let i=0; i<str.length; i++) hash = (hash<<5) - hash + str.charCodeAt(i); return Math.abs(hash) % this.size; }
    hash2(str) { let hash = 5381; for(let i=0; i<str.length; i++) hash = (hash * 33) ^ str.charCodeAt(i); return Math.abs(hash) % this.size; }
    hash3(str) { let hash = 0; for(let i=0; i<str.length; i++) hash = str.charCodeAt(i) + (hash << 6) + (hash << 16) - hash; return Math.abs(hash) % this.size; }
    
    getHashes(item) { return [this.hash1(item), this.hash2(item), this.hash3(item)].slice(0, this.hashCount); }
    
    add(item) {
        const hashes = this.getHashes(item);
        hashes.forEach(h => this.bitArray[h] = true);
    }
    
    check(item) {
        const hashes = this.getHashes(item);
        for(let h of hashes) {
            if(!this.bitArray[h]) return false; // Definitely not in set
        }
        return true; // Probably in set
    }
}

const blacklistBloom = new BloomFilter(1000, 3);
// Add some blacklisted drivers/packages
blacklistBloom.add("DRV-X99");
blacklistBloom.add("PKG-1042");
blacklistBloom.add("PKG-BAD");

function checkBloomFilter() {
    const val = document.getElementById('bloom-input').value.trim();
    if(!val) return;
    
    clearLog('bloom-terminal');
    log('bloom-terminal', `Generating hashes for "${val}"...`);
    const hashes = blacklistBloom.getHashes(val);
    log('bloom-terminal', `Hash indices: [${hashes.join(', ')}]`);
    
    const startTime = performance.now();
    const result = blacklistBloom.check(val);
    const timeTaken = performance.now() - startTime;
    
    if(result) {
        log('bloom-terminal', `Match found! ID is PROBABLY BLACKLISTED. Database check required. (${timeTaken.toFixed(3)}ms)`, "error");
    } else {
        log('bloom-terminal', `Clear. ID is DEFINITELY NOT blacklisted. No DB query needed. (${timeTaken.toFixed(3)}ms)`, "success");
    }
}


// ==========================================
// 3. K-MEANS CLUSTERING - DELIVERY ZONES
// ==========================================
let deliveryPoints = [];
let clusters = [];

function generateRandomOrders() {
    const n = parseInt(document.getElementById('kmeans-points').value);
    deliveryPoints = [];
    for(let i=0; i<n; i++) {
        // Find a random node to attach to
        const node = cityGraph.nodes[Math.floor(Math.random() * cityGraph.nodes.length)];
        // Add some jitter
        deliveryPoints.push({
            x: node.x + (Math.random()-0.5)*20,
            y: node.y + (Math.random()-0.5)*20,
            clusterId: -1
        });
    }
    drawMap();
    drawDeliveryPoints();
    clearLog('kmeans-terminal');
    log('kmeans-terminal', `Spawned ${n} random delivery points.`);
}

function drawDeliveryPoints() {
    const colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];
    
    deliveryPoints.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, Math.PI*2);
        ctx.fillStyle = p.clusterId === -1 ? '#fff' : colors[p.clusterId % colors.length];
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.stroke();
    });
    
    // Draw centroids
    clusters.forEach((c, i) => {
        ctx.beginPath();
        ctx.moveTo(c.x-8, c.y-8); ctx.lineTo(c.x+8, c.y+8);
        ctx.moveTo(c.x+8, c.y-8); ctx.lineTo(c.x-8, c.y+8);
        ctx.strokeStyle = colors[i % colors.length];
        ctx.lineWidth = 4;
        ctx.stroke();
    });
}

function runKMeans() {
    if(deliveryPoints.length === 0) return log('kmeans-terminal', "Generate points first!", "error");
    
    const k = parseInt(document.getElementById('kmeans-k').value);
    clearLog('kmeans-terminal');
    log('kmeans-terminal', `Initializing K-Means with K=${k}`);
    
    // Init centroids randomly from points
    clusters = [];
    let tempPoints = [...deliveryPoints];
    for(let i=0; i<k; i++) {
        const idx = Math.floor(Math.random()*tempPoints.length);
        clusters.push({ x: tempPoints[idx].x, y: tempPoints[idx].y });
        tempPoints.splice(idx, 1);
    }
    
    let iterations = 0;
    const maxIter = 20;
    let changed = true;
    
    // Simple async loop for animation
    function step() {
        if(!changed || iterations >= maxIter) {
            log('kmeans-terminal', `Converged in ${iterations} iterations.`, "success");
            return;
        }
        changed = false;
        
        // Assignment Step
        deliveryPoints.forEach(p => {
            let minDist = Infinity;
            let bestCluster = -1;
            clusters.forEach((c, i) => {
                const dist = Math.hypot(p.x - c.x, p.y - c.y);
                if(dist < minDist) { minDist = dist; bestCluster = i; }
            });
            if(p.clusterId !== bestCluster) {
                p.clusterId = bestCluster;
                changed = true;
            }
        });
        
        // Update Step
        clusters.forEach((c, i) => {
            let sumX = 0, sumY = 0, count = 0;
            deliveryPoints.forEach(p => {
                if(p.clusterId === i) { sumX += p.x; sumY += p.y; count++; }
            });
            if(count > 0) {
                c.x = sumX / count;
                c.y = sumY / count;
            }
        });
        
        iterations++;
        log('kmeans-terminal', `Iteration ${iterations} complete.`);
        drawMap();
        drawDeliveryPoints();
        setTimeout(step, 200); // 200ms delay for visual
    }
    step();
}

// ==========================================
// 4. GALE-SHAPLEY - STABLE MATCHING
// ==========================================
function runStableMatching() {
    clearLog('gs-terminal');
    log('gs-terminal', "Starting Gale-Shapley Stable Matching...");
    
    // Mocks: 3 Hubs (A, B, C) each wanting 2 drivers
    // 6 Drivers (D1-D6)
    const hubs = ['Hub A', 'Hub B', 'Hub C'];
    const hubCapacity = { 'Hub A': 2, 'Hub B': 2, 'Hub C': 2 };
    const drivers = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'];
    
    // Generate random preferences
    const driverPrefs = {};
    drivers.forEach(d => {
        driverPrefs[d] = [...hubs].sort(() => 0.5 - Math.random());
        log('gs-terminal', `${d} preferences: [${driverPrefs[d].join(', ')}]`);
    });
    
    const hubPrefs = {};
    hubs.forEach(h => {
        hubPrefs[h] = [...drivers].sort(() => 0.5 - Math.random());
        log('gs-terminal', `${h} preferences: [${hubPrefs[h].join(', ')}]`);
    });
    
    // Algorithm
    const unassignedDrivers = [...drivers];
    const assignments = { 'Hub A': [], 'Hub B': [], 'Hub C': [] }; // hub -> [driver]
    
    while(unassignedDrivers.length > 0) {
        const d = unassignedDrivers.shift();
        const prefHub = driverPrefs[d].shift(); // driver proposes to top remaining choice
        
        log('gs-terminal', `${d} proposes to ${prefHub}`);
        
        if(assignments[prefHub].length < hubCapacity[prefHub]) {
            // Hub has space
            assignments[prefHub].push(d);
            log('gs-terminal', `> ${prefHub} accepts ${d} (Has open slots)`);
        } else {
            // Hub is full, check if it prefers this driver over its worst current assigned driver
            const currentAssigned = assignments[prefHub];
            let worstDriver = currentAssigned[0];
            let worstRank = hubPrefs[prefHub].indexOf(worstDriver);
            let worstIdx = 0;
            
            for(let i=1; i<currentAssigned.length; i++) {
                const rank = hubPrefs[prefHub].indexOf(currentAssigned[i]);
                if(rank > worstRank) {
                    worstRank = rank;
                    worstDriver = currentAssigned[i];
                    worstIdx = i;
                }
            }
            
            const newDriverRank = hubPrefs[prefHub].indexOf(d);
            if(newDriverRank < worstRank) {
                // Hub prefers new driver
                assignments[prefHub].splice(worstIdx, 1);
                assignments[prefHub].push(d);
                unassignedDrivers.push(worstDriver); // worst driver gets kicked out
                log('gs-terminal', `> ${prefHub} swaps ${worstDriver} for ${d} (Prefers ${d})`);
            } else {
                // Hub rejects
                unassignedDrivers.push(d); // goes back to pool, will propose to next choice
                log('gs-terminal', `> ${prefHub} rejects ${d} (Prefers current team)`);
            }
        }
    }
    
    log('gs-terminal', "--- STABLE MATCHING COMPLETE ---", "success");
    for(let h in assignments) {
        log('gs-terminal', `${h} Team: [${assignments[h].join(', ')}]`, "highlight");
    }
}

// ==========================================
// 5. A* SEARCH - GPS ROUTING
// ==========================================
// Priority Queue Helper
class PriorityQueue {
    constructor() { this.items = []; }
    enqueue(item, priority) {
        this.items.push({item, priority});
        this.items.sort((a,b) => a.priority - b.priority);
    }
    dequeue() { return this.items.shift().item; }
    isEmpty() { return this.items.length === 0; }
}

function runAStarRouting() {
    clearLog('astar-terminal');
    
    // Find Hub A
    const startNode = cityGraph.nodes.find(n => n.isHub === 'A');
    // Pick random target
    const endNode = cityGraph.nodes[Math.floor(Math.random() * cityGraph.nodes.length)];
    
    log('astar-terminal', `Routing from Hub A (ID:${startNode.id}) to Target (ID:${endNode.id})`);
    
    // Adjacency list
    const adj = {};
    cityGraph.nodes.forEach(n => adj[n.id] = []);
    cityGraph.edges.forEach(e => {
        adj[e.u].push({v: e.v, weight: e.weight});
        adj[e.v].push({v: e.u, weight: e.weight}); // undirected for routing
    });
    
    const heuristic = (n1, n2) => Math.hypot(n1.x - n2.x, n1.y - n2.y);
    
    const openSet = new PriorityQueue();
    openSet.enqueue(startNode.id, 0);
    
    const cameFrom = {};
    const gScore = {};
    cityGraph.nodes.forEach(n => gScore[n.id] = Infinity);
    gScore[startNode.id] = 0;
    
    let nodesExplored = 0;
    const startTime = performance.now();
    
    while(!openSet.isEmpty()) {
        const curr = openSet.dequeue();
        nodesExplored++;
        
        if(curr === endNode.id) break; // Found path
        
        adj[curr].forEach(neighbor => {
            const tentative_g = gScore[curr] + neighbor.weight;
            if(tentative_g < gScore[neighbor.v]) {
                cameFrom[neighbor.v] = curr;
                gScore[neighbor.v] = tentative_g;
                const h = heuristic(cityGraph.nodes[neighbor.v], endNode);
                openSet.enqueue(neighbor.v, tentative_g + h);
            }
        });
    }
    
    const timeTaken = performance.now() - startTime;
    
    // Reconstruct path
    const path = [];
    let curr = endNode.id;
    while(cameFrom[curr] !== undefined) {
        path.unshift(curr);
        curr = cameFrom[curr];
    }
    path.unshift(startNode.id);
    
    log('astar-terminal', `A* Path found! Cost: ${gScore[endNode.id].toFixed(0)}`);
    log('astar-terminal', `Nodes explored: ${nodesExplored}`, "highlight");
    log('astar-terminal', `Time: ${timeTaken.toFixed(2)}ms`);
    
    // Draw
    drawMap();
    ctx.beginPath();
    ctx.moveTo(startNode.x, startNode.y);
    for(let i=1; i<path.length; i++) {
        const n = cityGraph.nodes[path[i]];
        ctx.lineTo(n.x, n.y);
    }
    ctx.strokeStyle = '#10b981'; // Green path
    ctx.lineWidth = 5;
    ctx.stroke();
    
    // Draw target marker
    ctx.beginPath();
    ctx.arc(endNode.x, endNode.y, 8, 0, Math.PI*2);
    ctx.fillStyle = '#10b981';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.stroke();
    
    // Store for dijkstra comparison
    window.lastRoute = { startNode, endNode, astarNodes: nodesExplored };
}

function compareDijkstra() {
    if(!window.lastRoute) return log('astar-terminal', 'Run A* first!', 'error');
    
    const { startNode, endNode, astarNodes } = window.lastRoute;
    
    const adj = {};
    cityGraph.nodes.forEach(n => adj[n.id] = []);
    cityGraph.edges.forEach(e => {
        adj[e.u].push({v: e.v, weight: e.weight});
        adj[e.v].push({v: e.u, weight: e.weight});
    });
    
    const pq = new PriorityQueue();
    pq.enqueue(startNode.id, 0);
    const dist = {};
    cityGraph.nodes.forEach(n => dist[n.id] = Infinity);
    dist[startNode.id] = 0;
    
    let nodesExplored = 0;
    const startTime = performance.now();
    
    while(!pq.isEmpty()) {
        const u = pq.dequeue();
        nodesExplored++;
        if(u === endNode.id) break;
        
        adj[u].forEach(neighbor => {
            const alt = dist[u] + neighbor.weight;
            if(alt < dist[neighbor.v]) {
                dist[neighbor.v] = alt;
                pq.enqueue(neighbor.v, alt);
            }
        });
    }
    
    const timeTaken = performance.now() - startTime;
    log('astar-terminal', `--- Dijkstra Comparison ---`);
    log('astar-terminal', `Dijkstra explored: ${nodesExplored} nodes`, "highlight");
    log('astar-terminal', `A* explored: ${astarNodes} nodes`, "success");
    log('astar-terminal', `Dijkstra Time: ${timeTaken.toFixed(2)}ms`);
    log('astar-terminal', `A* visits far fewer nodes because of the spatial heuristic!`);
}

// ==========================================
// 6. FORD-FULKERSON - MAX FLOW
// ==========================================
function bfsFlow(rGraph, s, t, parent) {
    const visited = new Array(cityGraph.nodes.length).fill(false);
    const queue = [];
    
    queue.push(s);
    visited[s] = true;
    parent[s] = -1;
    
    while(queue.length > 0) {
        const u = queue.shift();
        
        for(let v=0; v<cityGraph.nodes.length; v++) {
            if(!visited[v] && rGraph[u][v] > 0) {
                if(v === t) {
                    parent[v] = u;
                    return true;
                }
                queue.push(v);
                parent[v] = u;
                visited[v] = true;
            }
        }
    }
    return false;
}

function runMaxFlow() {
    clearLog('flow-terminal');
    
    const startNode = cityGraph.nodes.find(n => n.isHub === 'A');
    const endNode = cityGraph.nodes.find(n => n.isHub === 'C');
    
    log('flow-terminal', `Calculating Max Flow Capacity between Hub A and Hub C...`);
    
    const V = cityGraph.nodes.length;
    // Build adjacency matrix for capacities
    const rGraph = Array(V).fill(null).map(() => Array(V).fill(0));
    
    // We treat edges as directed from top-left to bottom-right for this flow
    // Or just directed both ways with same capacity. Let's do both ways.
    cityGraph.edges.forEach(e => {
        rGraph[e.u][e.v] = e.capacity;
        rGraph[e.v][e.u] = e.capacity; 
    });
    
    const parent = new Array(V);
    let maxFlow = 0;
    
    const startTime = performance.now();
    
    while(bfsFlow(rGraph, startNode.id, endNode.id, parent)) {
        let pathFlow = Infinity;
        // Find min capacity in path
        for(let v = endNode.id; v !== startNode.id; v = parent[v]) {
            let u = parent[v];
            pathFlow = Math.min(pathFlow, rGraph[u][v]);
        }
        
        // Update capacities in residual graph
        for(let v = endNode.id; v !== startNode.id; v = parent[v]) {
            let u = parent[v];
            rGraph[u][v] -= pathFlow;
            rGraph[v][u] += pathFlow;
        }
        
        maxFlow += pathFlow;
    }
    
    const timeTaken = performance.now() - startTime;
    
    log('flow-terminal', `Ford-Fulkerson Execution Complete. (${timeTaken.toFixed(2)}ms)`);
    log('flow-terminal', `Max Traffic Flow Capacity: ${maxFlow} vehicles/min`, "success");
    log('flow-terminal', `Edges that reached 0 residual capacity are the structural bottlenecks of the city.`);
    
    // Highlight bottlenecks
    drawMap();
    let bottlenecks = 0;
    cityGraph.edges.forEach(e => {
        // If original capacity > 0 but residual is 0 in either direction, it's a saturated edge
        if((e.capacity > 0 && rGraph[e.u][e.v] === 0) || (e.capacity > 0 && rGraph[e.v][e.u] === 0)) {
            const u = cityGraph.nodes[e.u];
            const v = cityGraph.nodes[e.v];
            ctx.beginPath();
            ctx.moveTo(u.x, u.y);
            ctx.lineTo(v.x, v.y);
            ctx.strokeStyle = '#ef4444'; // Red
            ctx.lineWidth = 4;
            ctx.stroke();
            bottlenecks++;
        }
    });
    log('flow-terminal', `Identified ${bottlenecks} saturated bottleneck roads (highlighted in red).`, "highlight");
}

"""

content = content.replace("</script>\n</body>", algorithms_js + "\n</script>\n</body>")

with open('/Users/ayushranjan/Documents/daa/index.html', 'w') as f:
    f.write(content)
