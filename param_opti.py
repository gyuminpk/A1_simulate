from netpyne import specs, sim
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import pylab
from neuron import h
import itertools



def calculate_max_firing_rate():
    return len(sim.allSimData.spkt)

def objective(params):
    # Update cell parameters based on params

    h.load_file("stdrun.hoc")

    netParams = specs.NetParams()  # object of class NetParams to store the network parameters

    cell_groups = 1
    cell_count = 1

    PYR_FS = {'secs': {}}
    PYR_FS['secs']['soma'] = {'geom': {}, 'pointps': {}}  # soma params dict
    PYR_FS['secs']['soma']['geom'] = {'diam': 10.0, 'L': 10.0, 'cm': 31.831}  # soma geometry
    PYR_FS['secs']['soma']['pointps']['Izhi'] = {  # soma Izhikevich properties
        'mod': 'Izhi2007b',
        'C': params['C'],
        'k': params['k'],
        'vr': -55,
        'vt': -40,
        'vpeak': 25,
        'a': 0.2,
        'b': -2,
        'c': -45,
        'd': -55,
        'celltype': 5}
    netParams.cellParams['PYR_FS'] = PYR_FS

    netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.05, 'tau2': 2.3, 'e': 0}  # AMPA
    netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 0.15, 'tau2': 15, 'e': 0}  # NMDA
    netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAA
    netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAB

    netParams.popParams['group'] = {'cellType': 'PYR_FS', 'numCells': cell_count,
                                    'yRange': [0 * cell_count, (1) * cell_count]}  # add dict with params for this pop

    netParams.stimSourceParams['Input'] = {'type': 'IClamp', 'del': 1e1, 'dur': 8e1,
                                           'amp': 0.4}  # Increased amp

    netParams.stimTargetParams['Input->group'] = {'source': 'Input', 'sec': 'soma', 'loc': 0.5,
                                                  'conds': {'pop': 'group', 'cellList': list(range(cell_count))},
                                                  'delay': 1, 'synMech': 'AMPA'}

    ## Simulation options
    sim_cfg = specs.SimConfig()  # object of class SimConfig to store simulation configuration

    sim_cfg.duration = 1 * 1e2  # Duration of the simulation, in ms
    sim_cfg.dt = 0.025  # Internal integration timestep to use
    sim_cfg.verbose = False  # Show detailed messages
    sim_cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}  # Dict with traces to record
    sim_cfg.recordCells = range(cell_groups * cell_count)
    sim_cfg.recordStep = 0.1  # Step size in ms to save data (e.g. V traces, LFP, etc)
    sim_cfg.filename = 'test'  # Set file output name
    sim_cfg.savePickle = False  # Save params, network and sim output to pickle file

    # Run simulation with amp = 0.2
    netParams.stimSourceParams['Input']['amp'] = 0.4
    sim.createSimulateAnalyze(netParams, sim_cfg)
    max_firing_rate_high_amp = calculate_max_firing_rate()

    netParams.stimSourceParams['Input']['amp'] = 0.2
    sim.createSimulateAnalyze(netParams, sim_cfg)
    max_firing_rate_1_amp = calculate_max_firing_rate()

    netParams.stimSourceParams['Input']['amp'] = 0.1
    sim.createSimulateAnalyze(netParams, sim_cfg)
    max_firing_rate_2_amp = calculate_max_firing_rate()


    # Run simulation with amp = 0
    netParams.stimSourceParams['Input']['amp'] = 0.0732
    sim.createSimulateAnalyze(netParams, sim_cfg)
    max_firing_rate_low_amp = calculate_max_firing_rate()

    # Objective function combining both conditions
    target_firing_rate_high = 14  # Target firing rate
    target_firing_rate_2 = 8  # Target firing rate
    target_firing_rate_1 = 4  # Target firing rate
    target_firing_rate_low = 2  # Target firing rate

    error_high_amp = abs(max_firing_rate_high_amp - target_firing_rate_high)/target_firing_rate_high
    error_1_amp = abs(max_firing_rate_1_amp - target_firing_rate_1)/target_firing_rate_1
    error_2_amp = abs(max_firing_rate_2_amp - target_firing_rate_2)/target_firing_rate_2
    error_low_amp = abs(max_firing_rate_low_amp - target_firing_rate_low)/target_firing_rate_low  # Should be close to 0

    return error_high_amp + error_2_amp + error_1_amp + error_low_amp

# Example usage with Hyperopt
from hyperopt import fmin, tpe, hp, Trials

# Define the search space
space = {
    'C' : hp.uniform('C', 0, 10),
    'k' : hp.uniform('k', 0, 100),
    # 'c' : hp.uniform('c', -200, 0),
    # 'd' : hp.uniform('d', -100, 200),

}

# Run optimization
trials = Trials()
best = fmin(objective, space, algo=tpe.suggest, max_evals=1000, trials=trials)
print("Best parameters:", best)
