from netpyne import specs, sim
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import pylab
from neuron import h
import itertools

def param_simul(input, cellType):
    netParams = specs.NetParams()  # object of class NetParams to store the network parameters

    cell_groups = 1
    cell_count = 1
    simul_dur = 1

    # Cell parameters
    ## PYR cell properties

    PYR_RS = {'secs': {}}
    PYR_RS['secs']['soma'] = {'geom': {}, 'pointps': {}}  # soma params dict
    PYR_RS['secs']['soma']['geom'] = {'diam': 5.0, 'L': 15.0, 'cm': 31.831}  # soma geometry
    PYR_RS['secs']['soma']['pointps']['Izhi'] = {  # soma Izhikevich properties
        'mod': 'Izhi2007b',
        'C': 1,
        'k': 0.7,
        'vr': -60,
        'vt': -40,
        'vpeak': 35,
        'a': 0.03,
        'b': -2,
        'c': -50,
        'd': 100,
        'celltype': 1}
    netParams.cellParams['PYR_RS'] = PYR_RS

    PYR_FS = {'secs': {}}
    PYR_FS['secs']['soma'] = {'geom': {}, 'pointps': {}}  # soma params dict
    PYR_FS['secs']['soma']['geom'] = {'diam': 10.0, 'L': 10.0, 'cm': 31.831}  # soma geometry
    PYR_FS['secs']['soma']['pointps']['Izhi'] = {  # soma Izhikevich properties
        'mod': 'Izhi2007b',
        'C': 0.2,
        'k': 1,
        'vr': -55,
        'vt': -40,
        'vpeak': 25,
        'a': 0.2,
        'b': -2,
        'c': -45,
        'd': -55,
        'celltype': 5}
    netParams.cellParams['PYR_FS'] = PYR_FS

    # Populartion Parameter
    netParams.popParams['group'] = {'cellType': f'PYR_{cellType}', 'numCells': cell_count,
                                    'yRange': [0 * cell_count,
                                               (1) * cell_count]}  # add dict with params for this pop


    if cellType == 'RS':
        simul_dur = 5e2

    elif cellType == 'FS':
        simul_dur = 1e2

    # Synaptic mechanism parameters
    netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.05, 'tau2': 2.3, 'e': 0}  # AMPA
    netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 0.15, 'tau2': 15, 'e': 0}  # NMDA
    netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAA
    netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAB
    # Stimulation parameters
    netParams.stimSourceParams['Input'] = {'type': 'IClamp', 'del': simul_dur*0.1, 'dur': simul_dur*0.8, 'amp': input}  # Increased amp

    netParams.stimTargetParams['Input->group'] = {'source': 'Input', 'sec': 'soma', 'loc': 0.5,
                                                  'conds': {'pop': 'group', 'cellList': list(range(cell_count))},
                                                  'delay': 1, 'synMech': 'AMPA'}

    ## Simulation options
    sim_cfg = specs.SimConfig()  # object of class SimConfig to store simulation configuration

    sim_cfg.duration = simul_dur  # Duration of the simulation, in ms
    sim_cfg.dt = 0.025  # Internal integration timestep to use
    sim_cfg.verbose = False  # Show detailed messages
    sim_cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}  # Dict with traces to record
    sim_cfg.recordCells = range(cell_groups * cell_count)
    sim_cfg.recordStep = 0.1  # Step size in ms to save data (e.g. V traces, LFP, etc)
    sim_cfg.filename = 'test'  # Set file output name
    sim_cfg.savePickle = False  # Save params, network and sim output to pickle file

    ## Create network and run simulation
    sim.createSimulateAnalyze(netParams=netParams, simConfig=sim_cfg)

    V_soma = sim.allSimData['V_soma']['cell_0']
    t = sim.allSimData['t']
    spkt = sim.allSimData['spkt']
    return [V_soma, t, spkt]

simul_set = {
    'FS' : [0.4, 0.2, 0.1, 0.0732],
    'RS' : [0.1, 0.085, 0.07, 0.06]
}

for cellType in simul_set:
    fig, axes = plt.subplots(4, 1, figsize=(5, 18))
    for index, input in enumerate(simul_set[cellType]):
        if cellType == "FS":
            input = input * 5
        simul_result = param_simul(input, cellType)
        axes[index].plot(simul_result[1], simul_result[0])
        # for spk_t in simul_result[2]:
        axes[index].vlines(simul_result[2], -70, -60, color = 'r')
        axes[index].set_title(f'{input}nA')
    plt.suptitle(f'{cellType} Neuron Voltage trace')
    plt.savefig(f'{cellType}.png')

