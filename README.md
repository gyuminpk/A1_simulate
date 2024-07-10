# A1_simulate

## Neuron Model
Izhi2007b - To simulate RS (regular spiking), FS (fast spiking) neurons 

(reference: https://modeldb.science/39948?tab=1 / Dynamical Systems in Neuroscience(DNS), Eugene M. Izhikevich)

## Neuron type
RS : FS = 4 : 1 (proportion for the number of neurons)

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
