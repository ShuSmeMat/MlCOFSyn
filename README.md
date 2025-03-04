# MlCOFSyn

<img alt="Static Badge" src="https://img.shields.io/badge/c++-8.1.0-red?style=flat"> <img alt="Static Badge" src="https://img.shields.io/badge/python-3.12-blue?style=flat"> <img alt="Static Badge" src="https://img.shields.io/badge/PyQt5-green?style=flat"> <img alt="Static Badge" src="https://img.shields.io/badge/sklearn-1.4.2-black?style=flat"> <img alt="Static Badge" src="https://img.shields.io/badge/numpy-1.26.4-pink?style=flat"> <img alt="Static Badge" src="https://img.shields.io/badge/pandas-2.2.2-orange?style=flat">
![Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-brown.svg)
![Windows Badge](https://img.shields.io/badge/Platform-Windows-blue)

MlCOFSyn is a machine learning framework designed to assist in the synthesis of two-dimensional covalent organic frameworks (2D COFs). MlCOFSyn leverages efficient machine learning algorithms and features an intuitive graphical interface, enabling it to be run on consumer-grade computers by non-experts. The MlCOFSyn framework currently integrates the NEgen1o model as the computational engine and has the following functionalities:

1. ​**Prediction**​: Predicts the crystal size distributions based on the input monomer addition sequence.
2. ​**Design**​: Reverse-engineer the required monomer addition sequence for the target crystal size.
3. ​**Optimization**​: Optimizes the monomer addition sequence to produce larger crystals.

## Installation
1.You can clone the repository by running the following commands:
```bash
git clone https://github.com/studentgpt/MlCOFSyn.git
```

2.The required libraries can be installed by running the following command:

```bash
pip install -r requirements.txt
```


## Requirements for running MlCOFSyn
### Python Libraries
The following Python libraries must be installed:
- numpy
- pandas
- scipy
- scikit-learn
- matplotlib
- tqdm
- joblib
- psutil

### System Requirements
- **Operating System**: Windows  
- **CPU**: A minimum of 6 CPU cores is required.
- **C++ Version**: `C++ >= 8.1.0` must be installed.

## Instructions for running MlCOFSyn


### **1.Prediction Task**
**1.1 Run the following command to launch the the NEgen1o Graphical User Interface (GUI):** 
```bash
cd MlCOFSyn\prediction
```
```bash
python NEgen1_start.py
```


After starting up the GUI, you will see the **`System and Parameters`** Panel:

- **`Set COF Parameters`** Button: Click this button to set the parameters for the 2D COF, which can be determined through experimental measurements and reaction pathway analysis<sup>[1][2]</sup>.Default parameters are for COF-5.

- The **Initial System** Section: This section allows the user to define the initial conditions of the system, such as the initial volume, initial nuclei concentration, diameter, and height.

- The **Conditions to Add Monomer** Section: In this section, the user can input the **Monomer (core unit) Concentration** and the **Monomer Addition Sequence**. The latter is a list of the monomer volume added at each time (in L; **assuming core and linker monomers are already combined in solution before addition into the system**). Note that the NEgen1o model works under stoichiometric monomer ratios thus **only the concentration of the core monomer is needed for input**.

- Once the **Monomer Addition Sequence** is entered, you may click the `Check Input` button to check the **Number of Additions** and the **Total Volume to Add**.

The **monomer addition sequence** is a numeral list separated by commas. Examples include:

* `0.019,0.037,0.055,0.073,0.091,0.109,0.127,0.145,0.163,0.181` represents an increasing-rate addition sequence

* `1` represents a single addition (add all monomers at once)

![image1](https://github.com/studentgpt/MlCOFSyn/blob/main/image/NEgen1o_1_1.png)
<img src="https://github.com/studentgpt/MlCOFSyn/blob/main/image/function1.png" alt="image2" width="300" height="auto">

**1.2  `Run Computational Engine` panel:**

In this panel, you can start the calculation by clicking the `Run` button to execute the NEgen1o model, which is currently supported in MlCOFSyn. You can view detailed output information in the panel in real-time.

![image3](https://github.com/studentgpt/test1/blob/main/image/NEgen1o_3.png)

🚨 **Based on the input monomer addition sequence, a `nuc__1_0_x`(where x represents the number of additions in a monomer addition sequence) file will be automatically generated MlCOFSyn\negen1o directory. Remove this file before inputing a different monomer addition sequence in a new Prediction task.**

**1.3 By clicking `Get Result Summary` Button in the `Post Processing` Panel section, the user can view the results including the final crystal distribution.**
![image4](https://github.com/studentgpt/MlCOFSyn/blob/main/image/Negen1o_4.png)

### **2.Optimization Task**

**2.1 Run the following command to launch the Bayesian optimization interface:**
   ```bash
   cd MlCOFSyn\optimization
   ```
   ```bash
   python main_ui_optimization.py
   ```

**2.2** After launching the program, you will enter the **Bayesian Optimization GUI**. The user can modify the material parameters by clicking the **`Set COF parameters`** button.

**2.3** Set the parameters for monomer addition:

  1. The core monomer concentration can be typed in the **Monomer Concentration** window.

  2. **Load Monomer Addition Sequence Space File:**
     Upload the file containing the monomer addition sequence space to be optimized. This file is in CSV format with the following format:
  ```bash
     r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20
  
     0.062,0.109,0.082,0.025,0.165,0.147,0.131,0.146,0.102,0.031,0,0,0,0,0,0,0,0,0,0
  
     0.031,0.036,0.07,0.054,0.021,0.086,0.027,0.012,0.092,0.013,0.089,0.075,0.028,0.028,0.088,0.071,0.076,0.019,0.022,0.062

   ```
  - The first row indicates the addition times.
  - The remaining rows represent all specified monomer addition sequences.
  - You can find data examples in the file: `MlCOFSyn\optimization\space\all_space.csv`
  - **All monomer addition sequences in the `reaction_space.csv` must have the same number of length** (use 0 to fill empty additions).
  
  2. **Stop Conditions**:  
  - Input the **Maximum Number of Iterations**.  
  - Specify the **No-Improvement Criterion** as a stop condition.  
  
  3. **Start the Optimization**:  
     Once the **monomer addition sequence space file** is loaded and the **stop conditions** are set, click the **`Start Bayesian Optimization`** button to run the program.

The **Maximum Q value** and its corresponding **monomer addition sequence** will be displayed, and all other results will be saved to `optimization/result.csv`.
 


![bayesian1](https://github.com/studentgpt/test1/blob/main/image/bayesian_1.png)

🚨**The Candidates Per Iteration should be less than or equal to the number of cores n to avoid system overload.**

### **3.Design Task**
**3.1 Run the following command to launch the Bayesian Design GUI:**
```bash
cd MlCOFSyn\design\multibax-sklearn-main
   ```
```bash
python main_ui_design.py
   ```
**3.2** After launching the program, you will enter the **Bayesian Design GUI**. The user can modify the material parameters by clicking the **`Set COF parameters button`**.

**3.3** After entering the initial parameters, follow these steps to begin the Bayesian Design process:
1. The core monomer concentration can be typed in the Monomer Concentration window.

2.  **Load Monomer Addition Sequence Space File:**: The reaction space format for the **Bayesian Design** task is the same as in the **Bayesian Optimization** task.

   You can find data examples in the file: `MlCOFSyn/design/multibax-sklearn-main/dataset/all_space.csv`
       
3. **Target Q range**：The target Q range that the user aims to achieve.
   
4. **Stop Conditions**:
   - Input the **Maximum Number of Iterations**.
   - Specify the **Number of Monomer Addition Sequences Found**.
   

**3.4** **Start the Design:** Once the **monomer addition sequence space file** is loaded and the **stop conditions** and **target Q range** are set, click the **`Start Bayesian Design`** button to run the program.
![design2](https://github.com/studentgpt/MlCOFSyn/blob/main/image/design2.png)

   
🚨**The Candidates Per Iteration should be less than or equal to the number of cores n to avoid system overload.**

## A brief description of the theory

The NEgen1 model<sup>[3]</sup> was derived from kinetic Monte Carlo simulation results. This model takes six parameters for the 2D COF and those for COF-5 are used as default as provided in the code.<sup>[3][4]</sup>Methods to derive the parameters for the other 2D COFs can be found in literature.<sup>[1][2]</sup> The NEgen1o model is optimized upon the NEgen1 model for efficiency while not affecting accuracy.<sup>[5]</sup>

The prediction task is performed by directly running the computational engine (currently the NEgen1o model). The optimization task leverages Bayesian algorithm.<sup>[6]</sup> The design task utilize the MeanBAX<sup>[7]</sup> as the acquisition function.

A detailed technical description can be found at: https://chemrxiv.org/engage/chemrxiv/article-details/67baeb0e81d2151a02a991ba and https://doi.org/10.1002/anie.202408937

## License
The Apache License 2.0 is a permissive license whose main conditions require the preservation of copyright and license notices. Contributors provide an express grant of patent rights. Licensed works, modifications, and larger works may be distributed under different terms and without source code.

| **Permissions**        | **Limitations**      | **Conditions**      |
|------------------------|----------------------|---------------------|
| Commercial use ✅       | Trademark use ❌      | License and copyright notice ⚠️ |
| Modification 	✅         | Liability ❌          | State changes ⚠️     |
| Distribution ✅         | Warranty ❌           |                     |
| Patent use ✅           |                      |                     |
| Private use ✅          |                      |                     |



## Authors

👤 **Yue Shi**

👤 **Jiaxin Tian**

👤 **Haoyuan Li**


## Contributing

Contributions, bug reports and feature requests are welcome!

Email: lihaoyuan@shu.edu.cn.

## Acknowledgments

This work was supported by the National Natural Science Foundation of China (grant number: 22103053).

## Citation

If you find this project helpful, please cite our papers:

1. **MlCOFSyn: A Machine Learning Framework to Facilitate the Synthesis of 2D Covalent Organic Frameworks**  
   DOI: [`https://chemrxiv.org/engage/chemrxiv/article-details/67baeb0e81d2151a02a991ba`](https://chemrxiv.org/engage/chemrxiv/article-details/67baeb0e81d2151a02a991ba)

2. **Taming Two-Dimensional Polymerization by a Machine-Learning Discovered Crystallization Model**  
   DOI: [`https://doi.org/10.1002/anie.202408937`](https://doi.org/10.1002/anie.202408937)
   ```
   @article{https://doi.org/10.1002/anie.202408937,
   author = {Tian, Jiaxin and Treaster, Kiana A. and Xiong, Liangtao and Wang, Zixiao and Evans, Austin M. and Li, Haoyuan},
   title = {Taming Two-Dimensional Polymerization by a Machine-Learning Discovered Crystallization Model},
   journal = {Angewandte Chemie International Edition},
   volume = {63},
   number = {39},
   pages = {e202408937},
   doi = {https://doi.org/10.1002/anie.202408937},
   url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/anie.202408937},
   eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/anie.202408937},
   year = {2024}
   }
   ```



## References

[1] Li, H.; Chavez, A. D.; Li, H.; Li, H.; Dichtel, W. R.; Bredas, J.-L. Nucleation and Growth of Covalent Organic Frameworks from Solution: The Example of COF-5. J. Am. Chem. Soc. 2017, 139 (45), 16310–16318.

[2]	Li, H.; Li, H.; Dai, Q.; Li, H.; Brédas, J.-L. Hydrolytic Stability of Boronate Ester-Linked Covalent Organic Frameworks. Adv. Theor. Simul. 2018, 1 (2), 1700015.

[3] Tian, J.; Treaster, K. A.; Xiong, L.; Wang, Z.; Evans, A. M.; Li, H. Taming Two-Dimensional Polymerization by a Machine-Learning Discovered Crystallization Model. Angew. Chem. Int. Ed. 2024, 63 (39), e202408937.

[4] Li, H.; Evans, A. M.; Dichtel, W. R.; Bredas, J.-L. Quantitative Description of the Lateral Growth of Two-Dimensional Covalent Organic Frameworks Reveals Self-Templation Effects. ACS Mater. Lett. 2021, 3 (4), 398–405.

[5] Shi Y, Tian J, Li H. MlCOFSyn: A Machine Learning Framework to Facilitate the Synthesis of 2D Covalent Organic Frameworks. ChemRxiv. 2025

[6] Shields, B. J.; Stevens, J.; Li, J.; Parasram, M.; Damani, F.; Alvarado, J. I. M.; Janey, J. M.; Adams, R. P.; Doyle, A. G. Bayesian Reaction Optimization as a Tool for Chemical Synthesis. Nature 2021, 590 (7844), 89–96.

[7] Chitturi, S. R.; Ramdas, A.; Wu, Y.; Rohr, B.; Ermon, S.; Dionne, J.; Jornada, F. H. da; Dunne, M.; Tassone, C.; Neiswanger, W.; Ratner, D. Targeted Materials Discovery Using Bayesian Algorithm Execution. npj Comput. Mater. 2024, 10 (1), 156.
