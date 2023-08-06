# cpmax Toolbox (deutsch)
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
- `to_vibA_import` - ermöglicht die Verarbeitung eines Pandas DataFrames zu einem für den vib.analyzer (V3.15) verständlichen Formats. 
    
- `cap_thres`- reduziert peaks oberhalb des Grenzwertes auf den Grenzwert (negative Werte werden auf negativen Grenzwert gesetzt)

- `filt_rot_thres`- filtert Umdrehungen mit Grenzwertüberschreitungen heraus

- `filt_rot_mean`- filtert Umdrehungen mit zu starker Mittelwertabweichung heraus

# cpmax Toolbox (english)
This package provides various data analysis and manipulation tools for cp.max Rotortechnik GmbH & Co. KG

## Quickstart
````Bash
pip install cpmaxToolbox
````

Up to now only the FilterTool can be used, which allows the processing of vibration data. This is included via 
````Python
import cpmaxToolbox.FilterTool as ft
````

In `example.ipynb` a data processing is presented as an example.


## FilterTool 
- `to_vibA_import` - allows to process a pandas DataFrame to a format understandable by the vib.analyzer (V3.15). 
    
- `cap_thres` - reduces peaks above the limit to the limit (negative values are set to negative limit)

- `filt_rot_thres` - filters out revolutions exceeding the limit value

- `filt_rot_mean` - filters out revolutions with too high mean value deviation