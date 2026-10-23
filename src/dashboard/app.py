

from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask, render_template

from detector.database import get_recent_flows, get_recent_alerts

PROJECT_ROOT = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(Path(__file__).resolve().parent / "templates"),
)


def kenya_time(timestamp):
    """Convert a UTC database timestamp to East Africa Time."""
    if not timestamp:
        return "—"

    utc_time = datetime.strptime(
        timestamp, "%Y-%m-%d %H:%M:%S"
    ).replace(tzinfo=timezone.utc)

    eat = utc_time + timedelta(hours=3)
    return eat.strftime("%d %b %Y, %I:%M:%S %p EAT")


@app.route("/")
def index():
    flows = get_recent_flows(20)
    alerts = get_recent_alerts(20)

    for flow in flows:
        flow["local_time"] = kenya_time(flow["timestamp"])

    for alert in alerts:
        alert["local_time"] = kenya_time(alert["created_at"])

    return render_template(
        "index.html",
        flows=flows,
        alerts=alerts,
        total_flows=len(flows),
        total_alerts=len(alerts),
        scan_count=sum(
            flow["prediction"] == "SCAN" for flow in flows
        ),
    )


if __name__ == "__main__":
    app.run(debug=True)
