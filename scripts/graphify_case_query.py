#!/usr/bin/env python3
"""
Graphify Case Query Engine
Provides programmatic and command-line access to the internal Case Study knowledge graph.
Strictly anonymous: no local drive paths or personal names.
"""

import sys
import os
import json
import argparse
from pathlib import Path

GRAPH_PATH = Path("graphify-out/graph.json")

def load_graph():
    if not GRAPH_PATH.exists():
        print(f"[!] Error: Graph file not found at {GRAPH_PATH}.")
        print("    Run: python -m graphify update . --no-cluster")
        sys.exit(1)
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_graph_summary():
    data = load_graph()
    nodes = data.get("nodes", [])
    edges = data.get("links", data.get("edges", []))
    
    # Analyze node types & modules
    subsystems = {}
    for n in nodes:
        nid = n.get("id", "")
        prefix = nid.split("_")[0] if "_" in nid else "root"
        subsystems[prefix] = subsystems.get(prefix, 0) + 1

    summary = {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "top_subsystems": sorted(subsystems.items(), key=lambda x: x[1], reverse=True)[:10]
    }
    return summary

def search_nodes(query: str, max_results: int = 15):
    data = load_graph()
    nodes = data.get("nodes", [])
    q = query.lower()
    
    matches = []
    for n in nodes:
        nid = n.get("id", "").lower()
        lbl = n.get("label", n.get("name", "")).lower()
        src = n.get("source", "").lower()
        
        score = 0
        if q in nid:
            score += 3
        if q in lbl:
            score += 2
        if q in src:
            score += 1
            
        if score > 0:
            matches.append((score, n))
            
    matches.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matches[:max_results]]

def get_node_connections(node_id: str):
    data = load_graph()
    edges = data.get("links", data.get("edges", []))
    
    outgoing = []
    incoming = []
    for e in edges:
        source = e.get("source")
        target = e.get("target")
        rel = e.get("relation", e.get("type", "relates_to"))
        
        if source == node_id:
            outgoing.append((rel, target))
        if target == node_id:
            incoming.append((rel, source))
            
    return {"outgoing": outgoing, "incoming": incoming}

def find_path(start_id: str, end_id: str, max_depth: int = 4):
    data = load_graph()
    edges = data.get("links", data.get("edges", []))
    
    # Build adjacency list
    adj = {}
    for e in edges:
        u = e.get("source")
        v = e.get("target")
        if u not in adj:
            adj[u] = []
        if v not in adj:
            adj[v] = []
        adj[u].append((v, e.get("relation", "relates_to")))
        adj[v].append((u, f"inv_{e.get('relation', 'relates_to')}"))

    # BFS for shortest path
    from collections import deque
    queue = deque([[start_id]])
    visited = {start_id}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == end_id:
            return path
        
        if len(path) <= max_depth:
            for neighbor, _ in adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
                    
    return None

def main():
    parser = argparse.ArgumentParser(description="Graphify Internal Case Study Query Engine")
    parser.add_argument("--summary", action="store_true", help="Print overall graph statistics and subsystem breakdown")
    parser.add_argument("--query", "-q", type=str, help="Search the knowledge graph for matching concepts or files")
    parser.add_argument("--explain", "-e", type=str, help="Explain connections and neighbors for a specific node ID")
    parser.add_argument("--path", "-p", nargs=2, metavar=("START", "END"), help="Find shortest path between two nodes")
    
    args = parser.parse_args()
    
    if args.summary:
        s = get_graph_summary()
        print("=== GRAPHIFY CASE STUDY INTERNAL KNOWLEDGE GRAPH ===")
        print(f"Total Nodes: {s['total_nodes']:,}")
        print(f"Total Edges: {s['total_edges']:,}")
        print("\nTop Subsystems in Graph:")
        for prefix, count in s["top_subsystems"]:
            print(f"  - {prefix}: {count:,} entities")
        return
        
    if args.query:
        results = search_nodes(args.query)
        print(f"=== SEARCH RESULTS FOR '{args.query}' ({len(results)} matches) ===")
        for idx, r in enumerate(results, 1):
            print(f"{idx}. [{r.get('id')}] -> {r.get('label', r.get('name', 'N/A'))}")
            print(f"   Source: {r.get('source', 'Unknown')} | Type: {r.get('type', r.get('kind', 'Unknown'))}")
        return

    if args.explain:
        node_id = args.explain
        conns = get_node_connections(node_id)
        print(f"=== NODE CONNECTIONS FOR '{node_id}' ===")
        print(f"Outgoing ({len(conns['outgoing'])}):")
        for rel, tgt in conns["outgoing"][:15]:
            print(f"  --[{rel}]--> {tgt}")
        print(f"Incoming ({len(conns['incoming'])}):")
        for rel, src in conns["incoming"][:15]:
            print(f"  <--[{rel}]-- {src}")
        return

    if args.path:
        start, end = args.path
        route = find_path(start, end)
        if route:
            print(f"=== SHORTEST PATH ({len(route) - 1} hops) ===")
            print(" -> ".join(route))
        else:
            print(f"No path found between '{start}' and '{end}' within search depth.")
        return

    parser.print_help()

if __name__ == "__main__":
    main()

