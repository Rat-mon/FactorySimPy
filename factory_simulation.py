import simpy

from factorysimpy.nodes.machine import Machine
from factorysimpy.edges.buffer import Buffer
from factorysimpy.nodes.source import Source
from factorysimpy.nodes.sink import Sink


def run_factory_simulation(simulation_time=40):
    env = simpy.Environment()

    source = Source(
        env,
        id="READING_SOURCE",
        flow_item_type="item",
        inter_arrival_time=0.8,
        blocking=False,
        out_edge_selection="RANDOM",
    )

    machine = Machine(
        env,
        id="COMMUNICATION_CHECK",
        work_capacity=4,
        processing_delay=1.1,
        blocking=False,
        in_edge_selection="RANDOM",
        out_edge_selection="RANDOM",
    )

    sink = Sink(env, id="RESULT_SINK")

    input_buffer = Buffer(
        env,
        id="INPUT_BUFFER",
        store_capacity=4,
        delay=0.5,
        mode="FIFO",
    )

    output_buffer = Buffer(
        env,
        id="OUTPUT_BUFFER",
        store_capacity=4,
        delay=0.5,
        mode="FIFO",
    )

    input_buffer.connect(source, machine)
    output_buffer.connect(machine, sink)

    env.run(until=simulation_time)

    print("\nFACTORYSIMPY SIMULATION")
    print(f"Simulation stopped at time {env.now}.")
    print("The production-line simulation has finished.")


if __name__ == "__main__":
    run_factory_simulation()
