# CYS-241L Lab 05 - Task 3: Dijkstra and A*
# This version needs NO external CSV files or extra libraries.
import csv, io, math, heapq

ROADS = '''origin,destination,distance
Karachi,Hyderabad,165
Karachi,Khuzdar,420
Karachi,Gwadar,640
Hyderabad,Sukkur,330
Sukkur,Quetta,430
Sukkur,Rahim Yar Khan,200
Khuzdar,Quetta,300
Khuzdar,Sukkur,390
Quetta,Dera Ghazi Khan,470
Gwadar,Khuzdar,620
Rahim Yar Khan,Bahawalpur,180
Bahawalpur,Multan,100
Multan,Dera Ghazi Khan,90
Multan,Sahiwal,175
Multan,Faisalabad,240
Dera Ghazi Khan,Dera Ismail Khan,230
Sahiwal,Lahore,180
Faisalabad,Lahore,130
Faisalabad,Sargodha,95
Sargodha,Islamabad,230
Faisalabad,Islamabad,300
Dera Ismail Khan,Sargodha,260
Dera Ismail Khan,Kohat,230
Lahore,Gujranwala,85
Lahore,Sialkot,125
Gujranwala,Sialkot,55
Gujranwala,Jhelum,160
Lahore,Islamabad,375
Jhelum,Rawalpindi,115
Rawalpindi,Islamabad,15
Islamabad,Peshawar,180
Rawalpindi,Peshawar,175
Peshawar,Mardan,60
Peshawar,Kohat,60
Kohat,Rawalpindi,200
Islamabad,Abbottabad,120
Abbottabad,Muzaffarabad,100
Rawalpindi,Muzaffarabad,140
Mardan,Abbottabad,130
Abbottabad,Gilgit,470
Gilgit,Skardu,240
Mardan,Gilgit,650
Jhelum,Muzaffarabad,200'''

COORDS = '''city,latitude,longitude
Karachi,24.8607,67.0011
Hyderabad,25.396,68.3578
Sukkur,27.7052,68.8574
Quetta,30.1798,66.975
Gwadar,25.1264,62.3225
Multan,30.1575,71.5249
Bahawalpur,29.3956,71.6836
Faisalabad,31.4504,73.135
Lahore,31.5204,74.3587
Sargodha,32.0836,72.6711
Gujranwala,32.1877,74.1945
Sialkot,32.4945,74.5229
Islamabad,33.6844,73.0479
Rawalpindi,33.5651,73.0169
Peshawar,34.0151,71.5249
Mardan,34.1989,72.0231
Abbottabad,34.1688,73.2215
Dera Ismail Khan,31.8626,70.9019
Muzaffarabad,34.37,73.4711
Gilgit,35.9208,74.308
Skardu,35.2971,75.6339
Sahiwal,30.6682,73.1114
Rahim Yar Khan,28.4202,70.2952
Khuzdar,27.8,66.6167
Dera Ghazi Khan,30.0489,70.6455
Jhelum,32.9425,73.7257
Kohat,33.5869,71.4414'''

graph = {}
for r in csv.DictReader(io.StringIO(ROADS)):
    a, b, w = r['origin'], r['destination'], float(r['distance'])
    graph.setdefault(a, {})[b] = w
    graph.setdefault(b, {})[a] = w
coords = {r['city']: (float(r['latitude']), float(r['longitude']))
          for r in csv.DictReader(io.StringIO(COORDS))}

def h(a, b):
    if a not in coords or b not in coords: return 0
    lat1, lon1 = map(math.radians, coords[a]); lat2, lon2 = map(math.radians, coords[b])
    x = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return 12742 * math.asin(min(1, math.sqrt(x)))

def search(g, start, goal, heuristic):
    q = [(heuristic(start, goal), 0, start)]
    dist, parent, expanded = {start: 0}, {}, 0
    while q:
        f, cost, city = heapq.heappop(q)
        if cost != dist.get(city): continue
        expanded += 1
        if city == goal:
            path = [goal]
            while path[-1] != start: path.append(parent[path[-1]])
            return path[::-1], cost, expanded
        for nxt, weight in g.get(city, {}).items():
            new = cost + weight
            if new < dist.get(nxt, float('inf')):
                dist[nxt], parent[nxt] = new, city
                heapq.heappush(q, (new + heuristic(nxt, goal), new, nxt))
    return None, float('inf'), expanded

print('TASK 3: INCIDENT-RESPONSE DISPATCH')
print('PART A - Dataset:', len(graph), 'cities,', sum(map(len, graph.values()))//2, 'roads')
print('Haversine estimate Lahore to Quetta:', round(h('Lahore','Quetta'), 1), 'km')
violations = [(a,b) for a in graph for b,w in graph[a].items() if a < b and h(a,b) > w + 1e-6]
print('Road-edge heuristic violations:', violations if violations else 'None')

trips = [('Lahore','Quetta'), ('Islamabad','Quetta'), ('Karachi','Lahore'), ('Peshawar','Quetta'), ('Sialkot','Sukkur')]
print('\nPART B - Dijkstra vs A*')
for s, t in trips:
    d = search(graph, s, t, lambda a,b: 0)
    a = search(graph, s, t, h)
    print(f'{s} -> {t}\n Dijkstra: {d[1]:.0f} km, {d[2]} expanded; path: {" -> ".join(d[0]) if d[0] else "No route"}')
    print(f' A*:       {a[1]:.0f} km, {a[2]} expanded; path: {" -> ".join(a[0]) if a[0] else "No route"}')

print('\nPART C - Overestimating heuristic (2 x Haversine)')
for s, t in trips:
    normal = search(graph, s, t, h); over = search(graph, s, t, lambda a,b: 2*h(a,b))
    print(f'{s} -> {t}: normal={normal[1]:.0f} km, doubled={over[1]:.0f} km')

print('\nPART D1 - Close roads on the Lahore-Quetta A* route')
path, original, _ = search(graph, 'Lahore', 'Quetta', h)
print('Original:', ' -> '.join(path), f'({original:.0f} km)')
for a, b in zip(path, path[1:]):
    w = graph[a].pop(b); graph[b].pop(a)
    alt = search(graph, 'Lahore', 'Quetta', h)
    print(f'Close {a}-{b}:', ' -> '.join(alt[0]) if alt[0] else 'No alternative route', '| distance:', alt[1])
    graph[a][b] = graph[b][a] = w

print('\nPART D2 - Cities with only one road')
leaves = [c for c in graph if len(graph[c]) == 1]
for c in leaves: print(c, '->', next(iter(graph[c])))
if not leaves: print('None')

print('\nPART D3 - Cybersecurity application')
print('A* can help incident-response teams plan a route to a known destination.')
print('Dijkstra finds shortest-distance routes without a heuristic. Update the graph when roads close.')
