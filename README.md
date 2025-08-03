# 📽️ Video Graph Summary

An end-to-end pipeline that transforms a video into a scene graph and allows natural language querying via a Generative AI-powered ReAct agent.

Inspired by the idea that different viewers perceive scenes differently, this project extracts frames from a video, generates captions, converts those into subject-predicate-object triples, builds a graph, and enables users to ask questions like:

> "Summarize this video from bunny point of view"

---

## 🧠 What This Project Does

- 🎞 **Frame Extraction** — Samples frames from video using OpenCV
- 🧠 **Scene Captioning** — Uses BLIP to describe visual content
- 🔗 **Triplet Extraction** — Extracts subject-predicate-object triples from captions using an LLM
- 🕸 **Graph Construction** — Builds a scene graph with NetworkX
- 🤖 **QA Agent** — ReAct agent with LangGraph + Structured Tools
- 🌐 **Streamlit Interface** — Preview videos, ask questions, and see agent/tool trace

---

## 🛠 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/ybshankar010/video-graph-summary.git
cd video-graph-summary
```

### 2. Create and activate virtual environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Download video and extract frames

```bash
python -m app.data.download_data
python  -m app.data.extract_frames
```

### 4. Generate captions and triples

```bash
python -m app.data.generate_summary
python -m app.data.extract_objects
```

### 5. Build scene graph

```bash
python -m app.graph.subject_predicate
```

### 6. Run Streamlit app

```bash
chmod +x launch.sh
./launch.sh
```

---

## 🤖 Agent Tools Supported

- `GetLabels` — List all node labels
- `GetEdges` — Return all graph edges
- `SearchEdges(keyword)` — Search edges by keyword
- `SummarizeSubgraph(node)` — Show all edges linked to a node

These tools are registered in the ReAct agent using `create_react_agent()` from LangGraph.

---

## 💡 Future Ideas

- Fuse visual scene graphs with transcript/audio
- Export graphs to Neo4j or RDF
- Extend to multi-modal summaries (video + text)
- Generate POV-based summaries from characters

---

## 📜 License

MIT License.

---

## 🙌 Acknowledgements

- [BLIP by Salesforce](https://huggingface.co/Salesforce/blip-image-captioning-base)
- [LangGraph (LangChain)](https://github.com/langchain-ai/langgraph)
- \[Qwen / DeepSeek / LLaMA3 open-source models]
- [Big Buck Bunny](https://peach.blender.org/) — sample video

---

## 📣 Article + Demo

- 📝 Blog: [https://ybshankar010.medium.com/the-bunny-the-fox-and-the-graph-building-a-video-qa-bot-038eb59f9d3a](https://ybshankar010.medium.com/the-bunny-the-fox-and-the-graph-building-a-video-qa-bot-038eb59f9d3a)
- 💻 Code: [https://github.com/ybshankar010/video-graph-summary](https://github.com/ybshankar010/video-graph-summary)
