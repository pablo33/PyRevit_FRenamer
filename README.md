# Quick info
This is a script for PyRevit.  
Done on Revit 2022.  
Multilingual.  

# What does this script do  
The script collec all structural foundations and informs the nearest grid intersection as the _Mark_ parameter. It  is a way to neme the structural foundations.  

The final name is composed as gridX.name + gridY.name.  
Grids do not have to be perpendicular neither parallel to X-Y axis, The script just calculate the nearest found grid intersection to name the _Mark_ foundation parameter.  

So it evalues the location point of the foundation and teh nearest grid intersection. The script selects the most horizontal grid as first on the name forming.  

# How to run the script  
This is a script for PyRevit. You can run it directly from the RevitPythonShell or you can setup as a bundle on your PyRevit installation.  

The script has been tested on Revit 2022 and it is multiligual.  

![Bundle button](https://proyectos33.ddns.net/media/pibucket/pablo/0001962-5be7325c_600.jpg "Mark parameter")  

![Bundle button](https://proyectos33.ddns.net/media/pibucket/pablo/0001963-5bf07b6e_600.jpg "Mark parameter")  


