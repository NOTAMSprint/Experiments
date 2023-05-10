# FPL Extraction

Here we try to identify all airports and FIRs that are relevant to a flight, by using the ICAO flightplan as a reference.

The flightplan string is provided in the standard format, for example:
```
(FPL-TAP036-IS
-A339/H-SADE1GHIJ1J3RWXYZ/LB1
-SBFZ0140
-M082F370 BOBAV2A BOBAV DCT MAGNO UN866 AMDOL/M082F370 UN866
 IREDO/M082F390 UN866 TENPA/M082F390 UN866 ORVEK/N0468F400 UN866
 BEXAL/N0461F380 DCT LIGRA LIGRA9A
-LPPT0644 LPFR
-PBN/A1B1C1D1L1O1S2 NAV/RNP2 COM/ACAS II SUR/260B DOF/230509
 REG/CSXXX EET/SBAO0036 GOOO0137 BUXON0205 NELTO0217 GVSC0256
 AMDOL0257 IREDO0327 TENPA0400 GCCC0402 GMMM0533 LPPC0618 SEL/DKBM
 CODE/4952AD OPR/TAP PER/D RALT/SBFZ GVAC TALT/SBSG RVR/550 RMK/)
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
 'firs': ['SBAO', 'GOOO', 'GVSC', 'GCCC', 'GMMM', 'LPPC'],
 'ralts': ['SBFZ', 'GVAC'],
 'talt': 'SBSG'}
```

## ⚠️ Known issues

1. The FIR of the departure airport is not included in field 18, and therefore need to be figured out another way
2. The FIR of the en-route alternates might not be crossed by the flight path, so it might not always be included.

## 💡 Ideas for features

- We could extract the validity boundaries of the NOTAM as well, in order to inform the sorting and filtering mechanism.

## Have requests or questions?

Write in Slack! `#-step1-notam-source`