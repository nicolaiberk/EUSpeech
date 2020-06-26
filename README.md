# EUSpeech
## Code of EUSpeech data collection

This repository is designed to give users of and contributors to the EUSpeech data an idea about how it was collected.

The code is structured as follows:
- The code used to collect [the original EUSpeech dataset](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XPCVEI) can be found in the [**EUSpeech V1**](https://github.com/nicolaiberk/EUSpeech/tree/master/EUSpeech%20V1)-folder.
- the code for the upcoming release of additional data is found in [**EUSpeech V2**](https://github.com/nicolaiberk/EUSpeech/tree/master/EUSpeech%20V2).
  - [**Original**](https://github.com/nicolaiberk/EUSpeech/tree/master/EUSpeech%20V2/Original) contains the code used for the first collection in summer 2019.
  - [**CovidUpdate**](https://github.com/nicolaiberk/EUSpeech/tree/master/EUSpeech%20V2/CovidUpdate) contains additional files of a collection in spring 2020.

Note that the mode of collection has changed substantively from the first version. If you want to collect additional data or look for a best practice to follow, please check out the [functions](https://github.com/nicolaiberk/EUSpeech/blob/master/EUSpeech%20V2/CovidUpdate/functions.py) file in the **CovidUpdate**-folder, which reflects our latest collection.