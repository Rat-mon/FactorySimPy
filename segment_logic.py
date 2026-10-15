from collections import defaultdict

NUMBER_OF_SEGMENTS = 31


def expected_connections():
    """Return every required directed neighbor connection."""
    connections = set()

    for segment in range(1, NUMBER_OF_SEGMENTS + 1):
        if segment > 1:
            connections.add((segment, segment - 1))

        if segment < NUMBER_OF_SEGMENTS:
            connections.add((segment, segment + 1))

    return connections


def evaluate_segments(observed_connections):
    """
    observed_connections contains (source, target) pairs
    that the device reports as successfully communicating.
    """
    expected = expected_connections()
    observed = set(observed_connections)

    # wrong segment numbers.
    for source, target in observed:
        if not (1 <= source <= NUMBER_OF_SEGMENTS):
            raise ValueError(f"Invalid source segment: {source}")
        if not (1 <= target <= NUMBER_OF_SEGMENTS):
            raise ValueError(f"Invalid target segment: {target}")

    results = {}

    for segment in range(1, NUMBER_OF_SEGMENTS + 1):
        required = {
            connection
            for connection in expected
            if connection[0] == segment
        }

        missing = required - observed

        results[segment] = {
            "status": 1 if not missing else 0,
            "expected_neighbors": sorted(
                target for source, target in required
            ),
            "missing_connections": sorted(missing),
        }

    return results


if __name__ == "__main__":
    # this would be replaced with actual device readings.
    demo_connections = expected_connections()

    # Simulate one failed connection: segment 3 -> segment 2.
    demo_connections.remove((3, 2))

    results = evaluate_segments(demo_connections)

    print("SEGMENT COMMUNICATION RESULTS")
    print("-" * 45)

    for segment, result in results.items():
        print(
            f"Segment {segment:02}: "
            f"Status = {result['status']} | "
            f"Neighbors = {result['expected_neighbors']}"
        )
