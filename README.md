# A1_simulate

## Neuron Model
Izhi2007b - To simulate RS (regular spiking), FS (fast spiking) neurons 

(reference: https://modeldb.science/39948?tab=1 / Dynamical Systems in Neuroscience(DNS), Eugene M. Izhikevich)

## Neuron type

<p align="center">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/74d641d9-70de-4c79-8cd8-bdec1d078ba8" width="50%" height="50%">
</p>
<div align="center">
  RS parameter
</div>


<p align="center">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/774402f9-4aa8-4669-b502-a7f11331f767" width="50%" height="50%">
</p>
<div align="center">
  FS parameter
</div>


(reference: https://modeldb.science/261423, DNS)

## Neuron Simulation / size definition

<p align="center">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/f6e7f2c2-47ec-4b2e-b7f8-66a3cf896e81" width="50%" height="50%">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/6193233f-6e9c-4ded-a958-4c0294caafd7" width="15%" height="23%">
</p>

<div align="center">
  Ideal / Simulated RS Neuron Electrophysics
</div>

<p align="center">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/41ee9777-4eec-4067-9f7c-cd74985cd562" width="50%" height="50%">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/88260b2b-73bf-4996-abec-df55ca7c168e" width="15%" height="23%">

</p>

<div align="center">
  Ideal / Simulated FS Neuron Electrophysics
</div>


There is small difference with the DNS's figure in terms of neuron rate, but it seems to simulate the rate variation pattern successfully.

(In the case of FS, change in the Izhi parameter only cannot make the proper simulated model, so I multiply 5 by the input current level.)

You can generate the voltage trace through **param_simul.py**, and parameter optimizing through **param_opti.py**

## Network Reference

I refered the Salvadord's paper that simulated macaque's auditory thalamocortical circuits using NetPyne.

(Data-driven multiscale model of macaque auditory thalamocortical circuits reproduces in vivo dynamics, Salvadord et al., 2023, [Link](https://www.cell.com/cell-reports/fulltext/S2211-1247(23)01390-6)


<p align="center">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/53d2a02b-b13f-4bdb-946d-9cd572f35fcd" width="80%" height="80%">
</p>

<div align="center">
  Dimensions of simulated A1 column with laminar cell densities, layer boundaries, cell morphologies, and distribution of populations
</div>

|Layer|E|SOM (somatostatin)|PV (Parvalbumin)|VIP|NGF|Relative Total Number|% of E| 
|------|---|---|---|---|---|---|---|
|Type|Excitatory|Inhibitory|Inhibitory|Inhibitory|Inhibitory|
|L1|-|-|-|-|48240|48240|0|
|L2|179784|2844|7110|8507|6055|204300|88|
|L3|179784|2844|7110|8507|6055|204300|88|
|L4|177744|2612|9907|1422|1530|193215|92|
|L5A|272160|16537|27994|4044|3318|324051|84|
|L5B|208413|16605|19849|2561|3628|251057|83|
|L6|142870|4493|5991|904|2727|156985|91|

<p align="center">
<img src="https://github.com/gyuminpk/A1_simulate/assets/171655753/40c5223d-2b72-4ef3-8fe3-9e2aaa0f1652" width="80%" height="80%">
</p>

<div align="center">
  Total neuron count and percentage of Exc neuron
</div>

So, I will build the A1 simulated network with above neuron proportion by layers.
I will use the RS, FS cell parameter for Exc, Inh neuron.

