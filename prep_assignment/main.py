#%% Init

from classiq import *
from mcx import mcx
import os

def test_mcx_k(k):
    @qfunc
    def main(ctrl: Output[QNum], target: Output[QBit]):
        
        allocate(k, ctrl)
        allocate(1, target)
        
        hadamard_transform(ctrl)
        mcx(k, ctrl, target)
    
    return main

def save_qprog(name, circ):
    with open(f"results/{name}.qprog", 'w') as f:
        f.write(circ)

 #%% Q1
test_mcx_func = test_mcx_k(5)
model=create_model(test_mcx_func)

width_model = set_constraints(model, Constraints(optimization_parameter=OptimizationParameter.WIDTH))
width_model_circ = synthesize(width_model)
depth_model = set_constraints(model, Constraints(optimization_parameter=OptimizationParameter.DEPTH))
depth_model_circ = synthesize(depth_model)
inbetween_model = set_constraints(model, Constraints(optimization_parameter=OptimizationParameter.DEPTH, max_width=7))
inbetween_model_circ = synthesize(inbetween_model)

save_qprog("q1_width", width_model_circ)
save_qprog("q1_depth", depth_model_circ)
save_qprog("q1_inbetween", inbetween_model_circ)

job = execute(width_model_circ)
results_width = job.result()[0].value.parsed_counts
circuit_width = QuantumProgram.from_qprog(width_model_circ).data.width
circuit_depth = QuantumProgram.from_qprog(width_model_circ).transpiled_circuit.depth
print(f"The circuit width is {circuit_width} and the circuit_depth is {circuit_depth}")
print(results_width)

job = execute(depth_model_circ)
results_depth = job.result()[0].value.parsed_counts
circuit_width = QuantumProgram.from_qprog(depth_model_circ).data.width
circuit_depth = QuantumProgram.from_qprog(depth_model_circ).transpiled_circuit.depth
print(f"The circuit width is {circuit_width} and the circuit_depth is {circuit_depth}")
print(results_depth)

job = execute(inbetween_model_circ)
results_inbetween = job.result()[0].value.parsed_counts
circuit_width = QuantumProgram.from_qprog(inbetween_model_circ).data.width
circuit_depth = QuantumProgram.from_qprog(inbetween_model_circ).transpiled_circuit.depth
print(f"The circuit width is {circuit_width} and the circuit_depth is {circuit_depth}")
print(results_inbetween)

#%% Q2 
test_mcx_func = test_mcx_k(20)
model=create_model(test_mcx_func)

width_model = set_constraints(model, Constraints(optimization_parameter=OptimizationParameter.WIDTH))
width_model_circ = synthesize(width_model)
depth_model = set_constraints(model, Constraints(max_width=25, optimization_parameter=OptimizationParameter.DEPTH))
depth_model_circ = synthesize(depth_model)

save_qprog("q2_width", width_model_circ)
save_qprog("q2_depth", depth_model_circ)


job = execute(width_model_circ)
results_width = job.result()[0].value.parsed_counts
circuit_width = QuantumProgram.from_qprog(width_model_circ).data.width
circuit_depth = QuantumProgram.from_qprog(width_model_circ).transpiled_circuit.depth
print(f"The circuit width is {circuit_width} and the circuit_depth is {circuit_depth}")

job = execute(depth_model_circ)
results_depth = job.result()[0].value.parsed_counts
circuit_width = QuantumProgram.from_qprog(depth_model_circ).data.width
circuit_depth = QuantumProgram.from_qprog(depth_model_circ).transpiled_circuit.depth
print(f"The circuit width is {circuit_width} and the circuit_depth is {circuit_depth}")

# %% Q3
import matplotlib.pyplot as plt

test_mcx_func = test_mcx_k(20)
base_model=create_model(test_mcx_func)

qnums = range(22,31)
models = [set_constraints(base_model, Constraints(max_width=qnum, optimization_parameter=OptimizationParameter.DEPTH)) for qnum in qnums]
circs = [synthesize(model) for model in models]
depths = [QuantumProgram.from_qprog(circ).transpiled_circuit.depth for circ in circs]

plt.plot(qnums, depths)

# %% plots

plt.figure(dpi=120)
plt.plot(qnums, depths, '.')
plt.xlabel('width')
plt.ylabel('depth')
plt.grid()
plt.savefig('results/q3_plot')
plt.show()

# %%
