import json
import networkx as nx
from pathlib import Path
from pyvis.network import Network
from app.utils.constants import TRIPLES_DIR, GRAPHS_DIR

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRIPLE_PATH = (PROJECT_ROOT / TRIPLES_DIR).resolve()
GRAPH_PATH = (PROJECT_ROOT / GRAPHS_DIR).resolve()
GRAPH_PATH.mkdir(parents=True, exist_ok=True)

def build_graph_from_triples(video_id, visualize=False):
    triple_file = TRIPLE_PATH / f"{video_id}_triples.json"
    graph_file = GRAPH_PATH / f"{video_id}.graphml"
    html_file = GRAPH_PATH / f"{video_id}.html"

    if not triple_file.exists():
        print(f"❌ Triple file not found for {video_id}")
        return

    G = nx.MultiDiGraph()

    with open(triple_file, "r") as f:
        data = json.load(f)
        for i, frame in enumerate(data):
            if not frame or not isinstance(frame, dict):
                print(f"Bad frame at index {i}:", frame)
                continue
            print("=" * 20)
            print(frame)
            triples = frame.get("triples", [])
            if not triples or not isinstance(triples, list):
                print(f"Bad triple in frame {frame.get('frame_id', 'unknown')}: {triple}")
                continue
            for triple in triples:
                if len(triple) == 3:
                    subj, pred, obj = triple
                    G.add_node(subj)
                    G.add_node(obj)
                    G.add_edge(subj, obj, label=pred)

    nx.write_graphml(G, graph_file)
    print(f"✅ Graph saved to {graph_file}")

    if visualize:
        net = Network(height="750px", width="100%", directed=True)
        for node in G.nodes:
            net.add_node(node, label=node)
        for u, v, d in G.edges(data=True):
            net.add_edge(u, v, label=d.get("label", ""))
        net.write_html(str(html_file), notebook=False, open_browser=True)
        print(f"🌐 Graph visualization written to {html_file}")

def build_all(visualize=False):
    for triple_file in TRIPLE_PATH.glob("*_triples.json"):
        video_id = triple_file.stem.replace("_triples", "")
        build_graph_from_triples(video_id, visualize=visualize)

if __name__ == "__main__":
    build_all(visualize=True)