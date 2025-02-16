# IOT-2
IOT Project 2: MODBUS attacks implementation based on : [_"Attack taxonomies for the Modbus protocols"_](https://doi.org/10.1016/j.ijcip.2008.08.003)



## Requirements 

- `pip install pymodbus v3.8.3`
- `pip install pyshark v0.6`
- `Wireshark` installed
- `Tshark` installed
- `python 3.9.* >=`

## How To Run Each Attack
**Python scripts** have to be run on **separate terminals** in the **order** noted below 

### Interception (B6)

- `cd InterceptionB6`
- `python B6_field.py`
- `python B6_attack.py`

### Interruption (T5)

- `cd InterruptionTC5`
- `python T5_field.py`
- `python T5_attack.py`

### Modification (B11)

- `cd ModificationB11`
- `python B11_field.py`
- `python B11_proxy.py`
- `python B11_sender.py`

### Fabrication (B2)

- `cd FabricationB2`
- `python B2_field.py`
- `python B2_replayer.py`
