# DelPhi4Py Private Repo (With DelPhi source code)

A python wrapper for the Poisson-Boltzmann Equation solver DelPhi

## Dependencies

- python3.5>=
- NumPy>=1.15.0

### DelPhi compilation dependencies

- gfortran #7.4.0
- gcc #7.4.0
- g++ #7.4.0
- libgfortran4

## Compilation

Before running the `compile.sh` script please check that the compiler paths exist and correspond to version 7

```bash
bash compile.sh
```
To check for a correct compilation please run the script `test.py` on delphi4py/example/ and see a "successful exit" message
```bash
cd example/; python3 test.py
```

## License

DelPhi4Py itself is distributed under a LGPL-3.0, however, DelPhi is
proprietary software. To use DelPhi the user is required to download the DelPhi license [here](https://honiglab.c2b2.columbia.edu/software/cgi-bin/software.pl?input=DelPhi)