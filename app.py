from security_guard import verify_agent_request

import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SurgeGuard-Agent",
    page_icon="🛡️",
    layout="wide",
)

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "reviewed" not in st.session_state:
    st.session_state.reviewed = set()

if "simulation_count" not in st.session_state:
    st.session_state.simulation_count = 0


# =========================================================
# HEADER
# =========================================================

st.title("🛡️ SurgeGuard-Agent")

st.caption(
    "AI-powered simulated risk alerts and inventory support"
)

st.info(
    "Educational prototype using fictional data only. "
    "Not for real clinical decisions or patient monitoring."
)


# =========================================================
# SIMULATION CONTROL
# =========================================================

st.divider()
st.header("🎛️ Simulation Control")

with st.form("simulation_form"):

    col1, col2 = st.columns(2)

    with col1:
        movement_mm = st.number_input(
            "Simulated movement (mm)",
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.5,
        )

        sensor_status = st.selectbox(
            "Simulated sensor status",
            ["NORMAL", "ABNORMAL"],
        )

    with col2:
        item = st.selectbox(
            "Supply item",
            [
                "gloves",
                "gauze packs",
                "general_supply_kits",
            ],
        )

        quantity = st.number_input(
            "Requested quantity",
            min_value=1,
            max_value=1000,
            value=5,
            step=1,
        )

    run_simulation = st.form_submit_button(
        "▶ Run Simulation",
        width="stretch",
    )


# =========================================================
# RUN SIMULATION
# =========================================================

if run_simulation:

    # Local fallback risk rule
    risk_result = (
        "REVIEW ALERT: Check the simulated data."
        if movement_mm >= 5 or sensor_status == "ABNORMAL"
        else "NORMAL: No demo rule was triggered."
    )

    # Fictional inventory
    stock_data = {
        "gloves": 20,
        "gauze packs": 10,
        "general_supply_kits": 5,
    }

    available_stock = stock_data[item]

    if quantity > available_stock:
        inventory_result = (
            f"LOW STOCK: Requested {quantity}, "
            f"but only {available_stock} units are available."
        )
    else:
        inventory_result = (
            f"STOCK AVAILABLE: {available_stock} units "
            f"available; requested {quantity}."
        )

    # Connect to Dify if an API key is configured
    api_key = os.getenv("DIFY_API_KEY")

    if api_key:

        try:
            response = requests.post(
                "https://api.dify.ai/v1/workflows/run",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": {
                        "movement_mm": movement_mm,
                        "sensor_status": sensor_status,
                        "arg1": item,
                        "arg2": quantity,
                    },
                    "response_mode": "blocking",
                    "user": "surgeguard-demo-user",
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()
            outputs = data.get("data", {}).get(
                "outputs", {}
            )

            # Use Dify outputs when returned
            risk_result = outputs.get(
                "risk_result",
                risk_result,
            )

            inventory_result = outputs.get(
                "inventory_result",
                inventory_result,
            )

        except (requests.RequestException, ValueError) as exc:
            st.warning(
                "Dify connection failed. The local demo "
                "results will be used instead."
            )
            st.caption(f"Connection detail: {exc}")

    else:
        st.warning(
            "DIFY_API_KEY is not configured. "
            "The app is using local demo rules."
        )

    # Determine whether this is an alert
    risk_text = str(risk_result)

    risk_alert = (
        movement_mm >= 5
        or sensor_status == "ABNORMAL"
        or "REVIEW ALERT" in risk_text.upper()
        or "HIGH" in risk_text.upper()
    )

    st.session_state.simulation_count += 1
    simulation_id = st.session_state.simulation_count

    # Store simulation in session history
    st.session_state.history.insert(
        0,
        {
            "id": simulation_id,
            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "movement": movement_mm,
            "sensor": sensor_status,
            "risk": risk_text,
            "risk_alert": risk_alert,
            "inventory": str(inventory_result),
            "item": item,
            "quantity": quantity,
        },
    )


# =========================================================
# SIMULATION RESULTS
# =========================================================

st.divider()
st.header("📊 Simulation Results")

if st.session_state.history:

    last = st.session_state.history[0]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Result")

        if last["risk_alert"]:
            st.error(last["risk"])
        else:
            st.success(last["risk"])

        st.write(
            f"Movement: {last['movement']:.1f} mm"
        )
        st.write(f"Sensor: {last['sensor']}")

    with col2:
        st.subheader("Inventory Check")
        st.write(f"Supply: {last['item']}")
        st.write(
            f"Requested quantity: {last['quantity']}"
        )
        st.write(last["inventory"])

else:
    st.info(
        "Run a simulation to see results here."
    )


# =========================================================
# PRIORITY ACTION CENTRE
# =========================================================

st.divider()
st.header("🎯 Priority Action Centre")

if st.session_state.history:

    alerts = [
        record
        for record in st.session_state.history
        if record["risk_alert"]
    ]

    pending_alerts = [
        record
        for record in alerts
        if record["id"] not in st.session_state.reviewed
    ]

    st.write(
        f"{len(pending_alerts)} action(s) need human review."
    )

    if not alerts:
        st.success("No risk alerts in this session.")

    for alert in alerts:

        alert_id = alert["id"]

        is_reviewed = (
            alert_id in st.session_state.reviewed
        )

        with st.container(border=True):

            st.subheader(
                f"Simulation #{alert_id}"
            )

            if is_reviewed:
                st.success("✅ Reviewed")
            else:
                st.warning("Review required")

            reasons = []

            if alert["movement"] >= 5:
                reasons.append(
                    "Movement reached or exceeded "
                    "the demo threshold of 5 mm."
                )

            if alert["sensor"] == "ABNORMAL":
                reasons.append(
                    "The simulated sensor status is ABNORMAL."
                )

            if not reasons:
                reasons.append(
                    "The demo workflow returned a review alert."
                )

            st.write(
                "**Why this alert appeared:** "
                + " ".join(reasons)
            )

            st.write(
                "**Suggested action:** Check the simulated "
                "inputs and verify the result."
            )

            if not is_reviewed:

                if st.button(
                    "Mark as reviewed",
                    key=f"review_{alert_id}",
                ):
                    st.session_state.reviewed.add(
                        alert_id
                    )
                    st.rerun()

else:
    st.caption(
        "Alerts will appear after you run a simulation."
    )


# =========================================================
# SMART INVENTORY FORECAST
# =========================================================

st.divider()
st.header("📦 Smart Inventory Forecast")

st.write(
    "Enter fictional stock quantities and daily usage "
    "to estimate how many days supplies may last."
)

supplies = [
    ("Gloves", 20, 2.0),
    ("Gauze packs", 10, 4.0),
    ("General supply kits", 5, 1.0),
]

with st.form("inventory_form"):

    stock_inputs = {}
    usage_inputs = {}

    for index, (name, default_stock, default_usage) in enumerate(
        supplies
    ):

        st.markdown(f"**{name}**")

        col1, col2 = st.columns(2)

        with col1:
            stock_inputs[name] = st.number_input(
                f"{name} — Current stock",
                min_value=0,
                max_value=100000,
                value=default_stock,
                step=1,
                key=f"forecast_stock_{index}",
            )

        with col2:
            usage_inputs[name] = st.number_input(
                f"{name} — Daily usage",
                min_value=0.0,
                max_value=100000.0,
                value=default_usage,
                step=0.5,
                key=f"forecast_usage_{index}",
            )

    calculate_forecast = st.form_submit_button(
        "🔍 Calculate Forecast",
        width="stretch",
    )

if calculate_forecast:

    st.subheader("Forecast Results")

    for name, _, _ in supplies:

        stock = stock_inputs[name]
        daily_usage = usage_inputs[name]

        st.markdown(f"### {name}")

        st.write(f"Current stock: {stock} units")
        st.write(
            f"Daily usage: {daily_usage:g} units"
        )

        if daily_usage == 0:

            st.info(
                "Daily usage is zero. "
                "Days remaining cannot be estimated."
            )

        else:

            days_left = stock / daily_usage

            st.metric(
                "Estimated days remaining",
                f"{days_left:.1f} days",
            )

            if stock == 0:
                st.error("No stock available in this demo.")

            elif days_left <= 3:
                st.warning(
                    f"Restock soon: {name}"
                )

            else:
                st.success(
                    f"Stock sufficient for now: {name}"
                )

st.caption(
    "Forecasts use fictional data and assume constant usage "
    "with no new deliveries."
)


# =========================================================
# DASHBOARD ANALYTICS
# =========================================================

st.divider()
st.header("📈 Dashboard Analytics")

total_simulations = len(st.session_state.history)

total_alerts = sum(
    1
    for record in st.session_state.history
    if record["risk_alert"]
)

reviewed_alerts = sum(
    1
    for record in st.session_state.history
    if record["risk_alert"]
    and record["id"] in st.session_state.reviewed
)

pending_alerts = total_alerts - reviewed_alerts

normal_results = total_simulations - total_alerts

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Simulations",
    total_simulations,
)

col2.metric(
    "Review Alerts",
    total_alerts,
)

col3.metric(
    "Reviewed Alerts",
    reviewed_alerts,
)

col4.metric(
    "Pending Alerts",
    pending_alerts,
)

st.subheader("Simulation Results Overview")

chart_df = pd.DataFrame(
    {
        "Result": ["Normal", "Review Alerts"],
        "Count": [normal_results, total_alerts],
    }
).set_index("Result")

st.bar_chart(chart_df)


# =========================================================
# DOWNLOAD SIMULATION REPORT
# =========================================================

st.divider()
st.header("📥 Download Simulation Report")

if st.session_state.history:

    report_rows = []

    for record in st.session_state.history:

        report_rows.append(
            {
                "Simulation ID": record["id"],
                "Timestamp": record["time"],
                "Movement (mm)": record["movement"],
                "Sensor Status": record["sensor"],
                "Risk Result": record["risk"],
                "Alert": (
                    "Yes"
                    if record["risk_alert"]
                    else "No"
                ),
                "Review Status": (
                    "Reviewed"
                    if record["id"]
                    in st.session_state.reviewed
                    else (
                        "Pending Review"
                        if record["risk_alert"]
                        else "No Review Required"
                    )
                ),
                "Supply Item": record["item"],
                "Requested Quantity": record["quantity"],
                "Inventory Result": record["inventory"],
            }
        )

    report_df = pd.DataFrame(report_rows)

    csv_data = report_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Download CSV Report",
        data=csv_data,
        file_name="surgeguard_simulation_report.csv",
        mime="text/csv",
        key="download_simulation_report",
        width="stretch",
        disabled=report_df.empty,
    )

    st.caption(
        "Click the button to download the current session's "
        "simulation history as a CSV file."
    )

else:
    st.info(
        "Run at least one simulation before downloading "
        "the report."
    )


# =========================================================
# SIMULATION HISTORY
# =========================================================

st.divider()
st.header("🕘 Simulation History")

if st.session_state.history:

    history_rows = []

    for record in st.session_state.history:

        history_rows.append(
            {
                "Simulation": record["id"],
                "Time": record["time"],
                "Movement (mm)": record["movement"],
                "Sensor": record["sensor"],
                "Risk Result": record["risk"],
                "Review Status": (
                    "Reviewed"
                    if record["id"]
                    in st.session_state.reviewed
                    else (
                        "Pending Review"
                        if record["risk_alert"]
                        else "No Review Required"
                    )
                ),
                "Supply": record["item"],
                "Quantity": record["quantity"],
            }
        )

    st.dataframe(
        pd.DataFrame(history_rows),
        width="stretch",
        hide_index=True,
    )

else:
    st.caption(
        "No simulations recorded yet."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "SurgeGuard-Agent | Educational prototype | "
    "Fictional data only | Human review required"
)
