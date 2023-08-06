# cpmax Toolbox
[English below]

Dieses Package stellt diverse Datenanalyse und -manipulationstools für cp.max Rotortechnik GmbH & Co. KG zur Verfügung. 

## Schnellstart
````Bash
pip install cpmaxToolbox
````

Bisher kann nur das FilterTool genutzt werden, welches eine die Verarbeitung von Schwingungsdaten ermöglicht. Dieses wird über 
````Python
import cpmaxToolbox.FilterTool as ft
````
eingebunden werden.

In `example.ipynb` wird beispielhaft eine Datenverarbeitung vorgestellt.


## FilterTool 
- Die Funktion `to_vibA_import` ermöglicht die Verarbeitung eines Pandas DataFrames zu einem für den vib.analyzer (V3.15) verständlichen Formats. 

- `cap_thres`

- `filt_rot_thres`

- `filt_rot_mean`

This Toolbox provides various data analysis and manipulation tools.
