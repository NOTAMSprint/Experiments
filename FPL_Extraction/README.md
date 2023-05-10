# FPL Extraction

Here we try to identify all airports and FIRs that are relevant to a flight, by using the ICAO flightplan as a reference.

The flightplan string is provided in the standard format, for example:
```
(FPL-TTT123-IS
-C550/L-SDE1E2GHIJ3J5RWZ/SB1D1
-KPWM1225
-N0440F310 SSOXS5 SSOXS DCT BUZRD
DCT SEY DCT HTO J174 ORF J121
CHS EESNT LUNNI1
-KJAX0214 KMCO
-PBN/A1L1B1C1D1O1T1 NAV/Z1 GBAS
DAT/1FANS2PDC SUR/260B RSP180
DOF/220501 REG/N123A SEL/BPAM
CODE/A05ED7)
```

The objective is to extract:

- Departure airport
- Take-off alternate
- Destination airport
- Destination alternate
- Enroute alternates
- FIRs crossed

The output is a Python dictionary with the following structure:
```python
{'adep': 'SBFZ',
 'ades': 'LPPT',
 'dalts': ['LPFR'],
 'firs': ['SBAO', 'GOOO', 'BUXO', 'NELT', 'GVSC', 'AMDO', 'IRED', 'TENP', 'GCCC', 'GMMM', 'LPPC'],
 'ralts': ['SBFZ', 'GVAC'],
 'talt': 'SBSG'}
```