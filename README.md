
NPR Shape-From-Shading techniques.
====

Sample implementations of Shape-From-Shading techniques for NPR.

* **Lumo: Illumination for Cel Animation** [Johnston et al. 2002]
    - Normal estimation from silhouettes.
* **Image-Based Material Editing** [Kahn et al. 2006]
    - Normal estimation from illumination.


## Result
### Under Construction
<!-- ### Lit-Sphere
![Lit-Sphere](LitSphere/results/LitSphere.png) -->

## Installation

Installation for **Windows** is slightly complicated due to the lack of package manager.

First, please install required python modules from http://www.lfd.uci.edu/~gohlke/pythonlibs/.

* NumPy: 1.8.2
* SciPy: 0.15.1
* matplotlib: 1.4.3rc1
* OpenCV: 2.4.10
* PyAMG: 2.2.1

.. code-block::

  // Launch VC 20xx command prompt
  $ python setup.py install

## Usage
### Directory Structure
* npr_sfs: main package.
    - methods: SFS main modules.
        - lumo.py: **Lumo** implementation.

## License

The MIT License 2015 (c) tody