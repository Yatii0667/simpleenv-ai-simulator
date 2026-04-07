from flask import Flask, jsonify
from env import SimpleEnv
import random 

app = Flask(__name__)
env = SimpleEnv()

current_state = None
score = 0

def run_episode(policy="rule"):
    state = env.reset()
    total = 0
    done = False
    actions = []

    while not done:
        if policy == "rule":
            if state == "hungry":
                action = "eat"
            elif state == "tired":
                action = "sleep"
            elif state == "exam":
                action = "study"
            else:
                action = "none"
        else:
            action = "none"

        actions.append(action)
        state, reward, done, _ = env.step(action)
        total += reward

    return actions, total

def random_episode():
    state = env.reset()
    total = 0
    done = False

    actions = ["eat", "sleep", "study"]

    while not done:
        action = random.choice(actions)
        state, reward, done, _= env.step(action)
        total += reward

        return total

@app.route("/")
def home():
    global current_state

    return f"""
    <h1>🧠 SimpleEnv AI Simulator</h1>
    <p><b>Current State:</b> {current_state}</p>

    <hr>
    <h3>🎮 Manual Play</h3>
    <a href="/reset"><button>Reset 🔄</button></a><br><br>
    <a href="/step/eat"><button>Eat 🍔</button></a>
    <a href="/step/sleep"><button>Sleep 😴</button></a>
    <a href="/step/study"><button>Study 📚</button></a>

    <hr>

    <h3>🤖 AI Evaluation</h3>
    <a href="/random"><button>Random Agent 🎲</button></a><br><br>
    <a href="/compare"><button>Compare Agents 📊</button></a><br><br>
    <a href="/agent"><button>Run AI Agent 🤖</button></a><br><br>
    <a href="/baseline"><button>Baseline Score 📊</button></a><br><br>
    <a href="/grader"><button>Final Score 🧠</button></a>
    <a href="/about"><button>About Project 📘</button></a><br><br>
    """

@app.route("/reset", methods=["GET", "POST"])
def reset():
    state = env.reset()
    return jsonify({"state": state})

@app.route("/step/<action>")
def step(action):
    global current_state, score
    next_state, reward, done, info = env.step(action)
    score += reward
    current_state = next_state
    return f"""
    <p>Action: {action}</p>
    <p>Reward: {reward}</p>
    <p>Total Score: {score}</p>
    <p>Next State: {next_state}</p>
    <p>Done: {done}</p>
    <br><a href="/">Go Back</a>
    """

@app.route("/baseline")
def baseline():
    _, total = run_episode()

    return jsonify({
        "score": total / len(env.tasks)})

@app.route("/random")
def random_agent():
    total = random_episode()

    return jsonify({
        "agent_type": "random",
        "normalized_score": total / len(env.tasks)
    })

@app.route("/agent")
def agent():
    actions, total = run_episode()

    return jsonify({
        "actions": actions,
        "total_score": total,
        "normalized_score": total / len(env.tasks)
    })

    actions_taken = []

    while not done:
        if state == "hungry":
            action = "eat"
        elif state == "tired":
            action = "sleep"
        elif state == "exam":
            action = "study"
        else:
            action = "none"

        actions_taken.append(action)

        state, reward, done, _ = env.step(action)
        total += reward

    return jsonify({
        "actions": actions_taken,
        "total_score": total,
        "normalized_score": total / len(env.tasks)
    })

    # Normalized score
    return jsonify({"score": total })

@app.route("/compare")
def compare():
    rule_total = run_episode()[1]
    random_total = random_episode()

    return jsonify({
        "environment": "SimpleEnv",
        "agents": {
            "rule_based": {
                "score": rule_total,
                "normalized": rule_total / len(env.tasks),
                "performance": "optimal"
            },
            "random": {
                "score": random_total,
                "normalized": random_total / len(env.tasks),
                "performance": "suboptimal"
            }
        },
        "conclusion": "Rule-based agent significantly outperforms random strategy"
    })

@app.route("/tasks")
def get_tasks():
    return jsonify({
        "tasks": ["hungry","tired","exam"],
        "actions": ["eat", "sleep", "study"]
    })

@app.route("/grader")
def grader():
    _, total = run_episode()

    return jsonify({
        "score": total / len(env.tasks)
    })
    normalized_score = baseline_score / len(env.tasks)
    return jsonify({"score": normalized_score})

@app.route("/about")
def about():
    return jsonify({
        "project": "SimpleEnv AI Simulator",
        "type": "Reinforcement Learning Simulation",
        "description": "An environment where agents take actions based on states and receive rewards.",
        "features": [
            "Manual gameplay",
            "Rule-based agent",
            "Random agent",
            "Performance comparison",
            "Reward-based evaluation"
        ],
        "goal": "To demonstrate decision-making and evaluation in AI systems"
    })

if __name__ == "__main__":
    app.run(debug=True)
