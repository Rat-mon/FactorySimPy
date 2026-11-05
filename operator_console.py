
import csv
import json
from datetime import datetime
from pathlib import Path

import streamlit as st


RESULTS_FILE = Path("segment_results.csv")
STATE_FILE = Path("alarm_state.json")

st.set_page_config(
    page_title="Operator Console",
    page_icon="OC",
    layout="wide"
)


def load_results():
    """Read the latest segment analysis."""
    if not RESULTS_FILE.exists():
        return []

    with RESULTS_FILE.open(
        newline="", encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def load_alarm_state():
    """Load persistent alarms and event history."""
    if STATE_FILE.exists():
        with STATE_FILE.open(
            encoding="utf-8"
        ) as file:
            return json.load(file)

    return {"active": {}, "events": []}


def save_alarm_state(state):
    """Save alarms so they survive console restarts."""
    with STATE_FILE.open(
        "w", encoding="utf-8"
    ) as file:
        json.dump(state, file, indent=4)


def log_event(state, event, segment, details):
    state["events"].append({
        "time": datetime.now().isoformat(
            timespec="seconds"
        ),
        "event": event,
        "segment": segment,
        "details": details
    })

    # Keep the most recent 500 events.
    state["events"] = state["events"][-500:]


def update_alarms(results, state):
    """Detect new faults and faults that have cleared."""

    current_failures = {}

    for row in results:
        if int(row["status"]) == 0:
            segment = int(row["segment"])
            missing = row["missing_connections"]

            signature = f"{segment}:{missing}"

            current_failures[signature] = {
                "segment": segment,
                "details": missing
            }

    previous = state["active"]
    updated = {}

    # Detect active and newly appearing faults.
    for signature, fault in current_failures.items():

        if signature in previous:
            updated[signature] = previous[signature]

        else:
            updated[signature] = {
                **fault,
                "acknowledged": False
            }

            log_event(
                state,
                "ALARM RAISED",
                fault["segment"],
                fault["details"]
            )

    # Detect faults that have cleared.
    for signature, fault in previous.items():

        if signature not in current_failures:
            log_event(
                state,
                "ALARM CLEARED",
                fault["segment"],
                fault["details"]
            )

    state["active"] = updated
    save_alarm_state(state)


def main():
    st.title("Operator Console")
    st.caption(
        "Spine Factory Simulation | "
        "Communication Monitoring System"
    )

    if st.button("Refresh"):
        st.rerun()

    results = load_results()

    if not results:
        st.warning(
            "No monitoring results found. "
            "Run main.py to generate segment_results.csv."
        )
        return

    state = load_alarm_state()
    update_alarms(results, state)

    passed = sum(
        int(row["status"]) == 1 for row in results
    )

    failed = len(results) - passed

    active_alarms = state["active"]

    unacknowledged = sum(
        not alarm["acknowledged"]
        for alarm in active_alarms.values()
    )

    # SUMMARY
    st.subheader("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Segments", len(results))
    col2.metric("PASS", passed)
    col3.metric("FAIL", failed)
    col4.metric("Unacknowledged Alarms", unacknowledged)

    st.divider()

    # ALARM PANEL
    st.subheader("Alarm Notification")

    if active_alarms:

        for signature, alarm in list(
            active_alarms.items()
        ):

            with st.container(border=True):

                st.error(
                    f"COMMUNICATION FAILURE - "
                    f"SEGMENT {alarm['segment']:02}"
                )

                st.write(
                    f"Missing connection: "
                    f"{alarm['details']}"
                )

                if alarm["acknowledged"]:
                    st.info("Acknowledged by operator.")

                else:
                    st.warning(
                        "Operator attention required."
                    )

                    if st.button(
                        "Acknowledge Alarm",
                        key=f"ack_{signature}"
                    ):
                        state["active"][signature][
                            "acknowledged"
                        ] = True

                        log_event(
                            state,
                            "ALARM ACKNOWLEDGED",
                            alarm["segment"],
                            alarm["details"]
                        )

                        save_alarm_state(state)
                        st.rerun()

    else:
        st.success(
            "No active communication alarms."
        )

    st.divider()

    # SEGMENT STATUS
    st.subheader("Segment Communication Status")

    for row in results:
        segment = int(row["segment"])
        status = int(row["status"])

        if status == 1:
            st.success(
                f"Segment {segment:02} - PASS"
            )
        else:
            st.error(
                f"Segment {segment:02} - FAIL | "
                f"Missing: {row['missing_connections']}"
            )

    st.divider()

    # EVENT HISTORY
    st.subheader("Evet History")

    if state["events"]:

        for event in reversed(state["events"][-50:]):
            st.write(
                f"**{event['time']}** | "
                f"{event['event']} | "
                f"Segment {event['segment']:02} | "
                f"{event['details']}"
            )

    else:
        st.info("No alarm events recorded.")

    st.caption(
        "Alarm acknowledgment does not clear a fault. "
        "A fault clears only when updated monitoring "
        "results show that the communication has recovered."
    )


if __name__ == "__main__":
    main()
