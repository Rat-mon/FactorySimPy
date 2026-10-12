import simpy
from factorysimpy.nodes.machine import Machine
from factorysimpy.edges.buffer import Buffer
from factorysimpy.nodes.source import Source
from factorysimpy.nodes.sink import Sink

env = simpy.Environment()

SRC = Source(
    env,
    id="SRC",
    flow_item_type="item",
    inter_arrival_time=0.8,
    blocking=False,
    out_edge_selection="RANDOM"
)

MACHINE1 = Machine(
    env,
    id="MACHINE1",
    work_capacity=4,
    processing_delay=1.1,
    blocking=False,
    in_edge_selection="RANDOM",
    out_edge_selection="RANDOM"
)

SINK = Sink(
    env,
    id="SINK"
)

BUF1 = Buffer(
    env,
    id="BUF1",
    capacity=4,
    delay=0.5,
    mode="FIFO"
)

BUF2 = Buffer(
    env,
    id="BUF2",
    capacity=4,
    delay=0.5,
    mode="FIFO"
)

BUF1.connect(SRC, MACHINE1)
BUF2.connect(MACHINE1, SINK)

env.run(until=10)

print("FactorySimPy simulation completed successfully.")