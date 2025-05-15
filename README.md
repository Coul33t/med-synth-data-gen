# RENEW

You'll need the datasets from the RENEW project, that you'll put in the `datasets` folder. Grab them [here](https://uncloud.univ-nantes.fr/index.php/s/SePD3YPPxFg2sbb)!

## Data generation
The bulk of this repository is in the `data_gen` folder.

### Required libraries
See the `requirements.txt` file
| Library name | Version tested |
|--------------|:--------------:|
| Numpy        | 1.22.1         |
| Pandas       | 1.4.1          |
| Scipy        | 0.19.1         |
| Matplotlib   | 3.5.1          |
| SDV          | 1.18.0         |

### Scripts
pre-requisites : 
    - Data CSV
    - Medication CSV

1. run the `clean_renew_data.py [optional data filename]` script on the original data. This will create a `{filename}_cleaned.csv` file.  
2. run the `sdv_gen.py [optional data filename] [optional metadata file name]` script. This will create a `{filename}_syn_data.csv` file, and also save the metadata and the trained model.  
3. Run the `post_process_syn_data.py [optional data filename]` script. This will smoothen the weights values with a sliding mean.  
4. Run the `add_medication_df.py` script  

### Optional & unused scripts
Optional:  
* `extend_data.py`: used to add a new boolean column indication if the patient has hypertension or not 

Unused:  
* `main.r`: used to generate synthetic data with the R `synthpop` package (using SDV for now)  
* `add_medication.py`: Not finished, used to add a medication  

### TODO
odds of the values going towards uncontrolled values 
1.04 -> it goes toward the higher risk of high pressure being uncontrolled
