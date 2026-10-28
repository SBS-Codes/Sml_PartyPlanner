# Smol Party Planner

Small examples of building AI agents with [smolagents](https://github.com/huggingface/smolagents), using an Ollama model through its OpenAI-compatible API, and recording agent activity with MLflow.

## Project files

- `sml_pp.py` — the party-planning agent. It uses `CodeAgent` with web search and webpage tools, plus custom tools for suggesting a menu, selecting a catering service, and generating a superhero party theme. The prompt asks the agent to calculate a party-ready time. It enables MLflow's smolagents autologging, so agent runs can be inspected as traces.
- `sml_add.py` — a minimal calculation example. It runs a `CodeAgent` to sum the numbers from 1 to 10 and enables MLflow smolagents autologging.
- `sml_weather.py` — a web-search example that asks for the current weather in Paris. It uses `DuckDuckGoSearchTool`; it does not currently enable MLflow autologging.
- `mlflow.db` — a local SQLite MLflow tracking database already present in this working copy. MLflow can create it when the tracking URI below is used. It is local run data, not application source, and is excluded from Git.
- `.gitignore` — excludes local Python environments/cache files and MLflow tracking data from Git.

## How smolagents and MLflow are used

The examples build `CodeAgent` instances from the smolagents library. Each agent is given a model (created with `OpenAIServerModel`, which connects to Ollama's OpenAI-compatible endpoint), a set of tools, and a step limit. The party planner combines built-in web tools with custom tools: functions decorated with `@tool` and a `Tool` subclass. The add and weather scripts show simpler calculation and search agents.

In `sml_pp.py` and `sml_add.py`, `mlflow.smolagents.autolog()` is called before the agent is created and run. MLflow captures the agent execution as trace data in the configured tracking store; the UI lets you inspect the trace after a run. `sml_weather.py` does not call autolog, so it does not produce MLflow traces as currently written.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) running locally, with a model available
- Internet access for the DuckDuckGo and webpage tools used by the examples

The scripts default to the Ollama model `llama:latest` at `http://localhost:11434/v1`. To use another Ollama model, set `OLLAMA_MODEL`; to use another compatible endpoint, set `OLLAMA_BASE_URL`. `MODEL_PROVIDER` currently supports only `ollama`.

## Install

From the project directory, create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "smolagents[toolkit]" openai mlflow
```

Install Ollama separately using its instructions for your operating system. Then, in one terminal, start Ollama and download the model:

```bash
ollama serve
ollama pull llama:latest
```

If you prefer a different installed model, for example `llama3.2`, set it before running a script:

```bash
export OLLAMA_MODEL=llama3.2
```

## Run the examples

Activate the virtual environment and set the MLflow tracking URI in the terminal where you run the examples. This makes agent runs and the MLflow UI use the same local SQLite database:

```bash
source .venv/bin/activate
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
```

Run any example from the project directory:

```bash
python sml_pp.py
python sml_add.py
python sml_weather.py
```

`sml_pp.py` and `sml_add.py` record runs with MLflow. `sml_weather.py` currently runs without MLflow tracing. The party planner's web tools and the weather example require an internet connection.

## View MLflow traces

After running either MLflow-enabled example, start the MLflow UI from the project directory in a separate terminal, using the same Python environment:

```bash
source .venv/bin/activate
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), choose the experiment containing the run, and open its **Traces** view to inspect the recorded agent execution. Keep the UI process running while viewing traces; stop it with `Ctrl+C` when finished.

## Configuration

| Environment variable | Default | Purpose |
| --- | --- | --- |
| `MODEL_PROVIDER` | `ollama` | Model provider. Only `ollama` is currently supported. |
| `OLLAMA_MODEL` | `llama:latest` | Ollama model name. |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama's OpenAI-compatible API endpoint. |
| `MLFLOW_TRACKING_URI` | MLflow default | Tracking store. Set to `sqlite:///mlflow.db` as shown above to use the project's local SQLite database. |

## Uploading to GitHub

Review the files before publishing. The provided `.gitignore` keeps `mlflow.db`, MLflow artifacts, virtual environments, and Python cache files out of new Git additions. Do not commit credentials or private tracking data.
