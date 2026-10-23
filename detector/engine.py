
from detector.predictor import predict_flow
from detector.database import save_flow, save_alert


def analyze_and_store(
    features,
    source_ip,
    destination_ip,
    source_port,
    destination_port,
    protocol,
    packet_count,
    total_bytes,
    duration,
):
    # 1. Classify the network flow using the trained model
    result = predict_flow(features)

    # 2. Save the prediction in the database
    flow_id = save_flow(
        source_ip=source_ip,
        destination_ip=destination_ip,
        source_port=source_port,
        destination_port=destination_port,
        protocol=protocol,
        packet_count=packet_count,
        total_bytes=total_bytes,
        duration=duration,
        prediction=result["prediction"],
        confidence=result["confidence"],
    )

    # 3. Create an alert if the model detects a scan
    if result["prediction"] == "SCAN":
        save_alert(
            flow_id=flow_id,
            alert_type="Port Scan Detection",
            severity="High",
            message=(
                f"Possible scan detected from {source_ip} "
                f"to {destination_ip}. "
                f"Scan probability: {result['scan_probability']:.2%}"
            ),
        )

    # 4. Return the result for the dashboard or testing
    return {
        "flow_id": flow_id,
        **result,
    }
