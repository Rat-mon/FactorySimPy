import csv
from pathlib import Path

from segment_logic import (
    NUMBER_OF_SEGMENTS,
    evaluate_segments,
    expected_connections,
)
from factory_simulation import run_factory_simulation


DATA_FILE = Path("device_readings.csv")


def load_device_readings():
    """Load successful directed connections from a CSV file."""
    connections = []

    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["positive"]) == 1:
                connections.append(
                    (
                        int(row["source_segment"]),
                        int(row["target_segment"]),
                    )
                )

    return connections


def main():
    print("31-SEGMENT COMMUNICATION MONITOR")
    print("=" * 40)

    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        connections = load_device_readings()
        print("Input: device_readings.csv")
    else:
        # Demonstration only; not real device data.
        connections = expected_connections()
        connections.remove((3, 2))
        print("Input: simulated demo data (not a real device)")

    results = evaluate_segments(connections)

    passed = sum(
        result["status"] == 1 for result in results.values()
    )
    failed = NUMBER_OF_SEGMENTS - passed

    print("\nSEGMENT RESULTS")
    for segment, result in results.items():
        print(
            f"Segment {segment:02}: "
            f"{'PASS' if result['status'] else 'FAIL'}"
        )

    print("\nSUMMARY")
    print(f"Total segments: {NUMBER_OF_SEGMENTS}")
    print(f"Passing segments: {passed}")
    print(f"Failing segments: {failed}")

    # Save the segment analysis.
    with open("segment_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "segment",
            "status",
            "expected_neighbors",
            "missing_connections",
        ])

        for segment, result in results.items():
            writer.writerow([
                segment,
                result["status"],
                ";".join(map(str, result["expected_neighbors"])),
                ";".join(
                    f"{source}->{target}"
                    for source, target
                    in result["missing_connections"]
                ),
            ])

    print("\nSaved results to segment_results.csv")

    # Run the discrete-event factory model.
    run_factory_simulation()


if __name__ == "__main__":
    main()
