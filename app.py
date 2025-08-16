import pandas as pd
import matplotlib.pyplot as plt
import io, base64
from flask import Flask, jsonify, request

app = Flask(__name__)

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded


# =======================
# GRADER ENDPOINT (weather)
# =======================
@app.route("/analyze", methods=["POST"])
def analyze():
    df = pd.read_csv("sample-weather.csv")

    # Core stats
    average_temp_c = float(df["temp_c"].mean())
    max_precip_date = str(df.loc[df["precip_mm"].idxmax(), "date"])
    min_temp_c = float(df["temp_c"].min())
    temp_precip_correlation = float(df["temp_c"].corr(df["precip_mm"]))
    average_precip_mm = float(df["precip_mm"].mean())

    # Line chart: temp over time
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["temp_c"], color="red")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (C)")
    temp_line_chart = fig_to_base64(fig)

    # Histogram: precipitation
    fig, ax = plt.subplots()
    ax.hist(df["precip_mm"], bins=10, color="orange")
    ax.set_xlabel("Precipitation (mm)")
    precip_histogram = fig_to_base64(fig)

    return jsonify({
        "average_temp_c": average_temp_c,
        "max_precip_date": max_precip_date,
        "min_temp_c": min_temp_c,
        "temp_precip_correlation": temp_precip_correlation,
        "average_precip_mm": average_precip_mm,
        "temp_line_chart": temp_line_chart,
        "precip_histogram": precip_histogram
    })


# ==========================
# CUSTOM ENDPOINT (your work)
# ==========================
@app.route("/multi-analyze", methods=["POST"])
def multi_analyze():
    dataset = request.json.get("dataset")

    if dataset == "sales":
        df = pd.read_csv("sample-sales.csv")
        summary = {
            "total_sales": float(df["sales"].sum()),
            "average_sales": float(df["sales"].mean()),
            "max_sales": float(df["sales"].max())
        }
        return jsonify({"dataset": "sales", "summary": summary})

    elif dataset == "network":
        df = pd.read_csv("sample-network.csv")
        summary = {
            "nodes": int(df["source"].nunique() + df["target"].nunique()),
            "edges": int(len(df)),
            "avg_weight": float(df["weight"].mean())
        }
        return jsonify({"dataset": "network", "summary": summary})

    elif dataset == "weather":
        df = pd.read_csv("sample-weather.csv")
        summary = {
            "average_temp_c": float(df["temp_c"].mean()),
            "average_precip_mm": float(df["precip_mm"].mean())
        }
        return jsonify({"dataset": "weather", "summary": summary})

    else:
        return jsonify({"error": "Unknown dataset"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


