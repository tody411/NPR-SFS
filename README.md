
NPR Shape-From-Shading techniques.
====

Sample implementations of Shape-From-Shading techniques for NPR.

* **Lumo: Illumination for Cel Animation** [Johnston et al. 2002]
    - Normal estimation from silhouettes.
* **Image-Based Material Editing** [Kahn et al. 2006]
    - Shape recovery section.


## Result
*Status*: Under construction.
<!-- ### Lit-Sphere
![Lit-Sphere](LitSphere/results/LitSphere.png) -->

## Installation

*Note*: This program was only tested on **Windows** with **Python2.7**.
**Linux** and **Mac OS** are not officially supported,
but the following instructions might be helpful for installing on those environments.

### Dependencies
Please install the following required python modules.

* **NumPy**
* **SciPy**
* **matplotlib**
* **OpenCV**
* **PyAMG**

As these modules are heavily dependent on NumPy modules, please install appropriate packages for your development environment (Python versions, 32-bit or 64bit).
For 64-bit Windows, you can download the binaries from [**Unofficial Windows Binaries for Python Extension Packages**](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

This program also uses **docopt** for CLI.
**docopt** will be installed automatically through the following **pip** command for main modules.

### Install main modules
You can use **pip** command for installing main modules.
Please run the following command from the shell.

``` bash
  > pip install git+https://github.com/tody411/NPR-SFS.git
```

## Usage
### Package Structure
* npr_sfs: Main package.
    - datasets: Utility module for small datasets.
    - methods: SFS main modules.

### CLI
Each method implementation in npr_sfs/methods provides **CLI** (provided by **docopt**) to run the program.
The following **CLI** examples can be tested from npr_sfs/methods directory.

**No args**: Simple demo with installed datasets.
``` bash
  > python lumo.py
```

**input**: You can specify an input image file as the command args.
``` bash
  > python lumo.py ../datasets/Blob1.png
```

**-o --output**: You can save estimated normal image (The output will be saved in the same directory as the input).

``` bash
  > python lumo.py -o
```

**-q --quiet**: Quiet mode (GUIs are not shown).
``` bash
  > python lumo.py -q -o
```

## Future work:

* [ ] Update results.
* [ ] Implement more methods.
* [ ] Comparison module for summarizing the results.

## License

The MIT License 2015 (c) tody