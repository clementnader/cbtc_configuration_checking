# DC_TU VERIFICATION TOOL

This tool helps with the **ADD_VERIF_014 (for v6) or ADD_VERIF_024 (for v7)** additional verification about the DC_TU files at SA level asked by the *Onboard DPSA* (C11_D412) in §4.6.

---
## 1. Description of the Verification of the DC_TU files activity
The Verification of the DC_TU files activity is described in ADD_VERIF_014 (for v6) or ADD_VERIF_024 (for v7) in §4.6 of Onboard DPSA. <br />
The objective to verify the unicity of PMC encryption keys and PMC addresses, and that these addresses are in the CBTC network (meaning that they correspond to the IP Addressing Plan).

**ADD_VERIF_XXX**:
> All "DC_TU.csv" delivered files (under Delivery directory\CC_PARAMETERS\TrainUnit_x) shall be checked by the Specific Application RAMS DATA review versus [CC STS] expressed need REQ_C11_D411_11813 regarding the use the TCP/IP of SSL based protocol:
> - Each PMC shall have an address on the CBTC network.
> - Each PMC shall have a unique encryption key. The key shall be diversified according:
>   - The line, town and project where the CC is running,
>   - The CC ID,
>   - The CC hardware version,
>   - The PMC number (that means there is 3 keys per CC unit),
> 
> That means especially that for each "DC_TU.csv" delivered files, for each CC'x'_ID to be installed, and for each PMC'y' with y = 1 or 2 or 3, then each CC'x'_PMC'y'_SSH_RSA_PUBLIC_KEY shall have a unique value, with no noticed collision with others CC'x'_PMC'y'_SSH_RSA_PUBLIC_KEY.

---
## 2. Tool behavior
The tool automates the verification of the unicity of the PMC alpha and beta IP Addresses and of the PMC SSH public keys. The correspondence of the addresses with the IP Plan is left to verify manually.

---
## 3. How to use the tool

### 3.1. Inputs to launch the tool
- <ins>**C11_D470**</ins>: It is the path to the project CC kit C11_D470.

---
### 3.2. Steps to use the tool to verify the DC_TU files:

0. A preliminary step to take once in order to install the required Python libraries:
   - Modify the file "**install_python_modules.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name. <br />
 (for python.exe -> "set PYTHON_EXE=python", for python39.exe -> "set PYTHON_EXE=python39", etc.)
   - Launch "**install_python_modules.bat**". This executable will **install the required Python libraries**. <br />
 If an error occurs saying that pip is not installed, try to launch the command "python39 -m ensurepip --default-pip" (to update with the name or your Python 3.9 executable). It will install the default version of pip. <br />
 If a proxy error occurs, try to modify the line "%PYTHON_EXE% -m pip install %%x --proxy http://z-proxy1.loc.global.sys" to remove the proxy argument at the end and try to use a local network (disconnect from the VPN or from office network). (The proxy address is working in Hitachi France network.)


1. Modify the file "**dc_tu_verification.bat**" to add to the PATH your Python 3.9 executable and modify the PYTHON_EXE variable to match your Python 3.9 executable name.


2. Launch "**dc_tu_verification.bat**". It will launch the Python script to check the verify the DC_TU files.


3. A window will appear and ask for the path to the project **C11_D470 directory**.


4. Once all the information has been specified, you can press the button **"Launch DC_TU Verification"**.


5. The result Excel file is placed into the Desktop and is opened automatically.

---
### 3.3 Results
The tool generates an Excel verification file. The aim is to use this file as an attachment to the Onboard DPSR for the analysis of the corresponding ADD_VERIF_XXX about the DC_TU.csv files.

Sheet **"PMC_IP_Address"** contains the list of the alpha and beta IP addresses for PMC 1, 2 and 3 for all train units.

Sheet **"PMC_SSH_Key"** contains the list of the SSH public keys for PMC 1, 2 and 3 for all train units. 

A conditional formatting rule is set to identify if an entry is appearing multiple times and thus a KO. <br />
The column Unicity is filled by the tool and a KO is raised if an entry corresponds to a previous entry. <br />
In sheet **"PMC_IP_Address"**, the column *Correspondence with IP Addressing Plan* is left empty and is to be filled by the user manually.
