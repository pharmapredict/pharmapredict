# PharmaPredict
Based on [historical data](https://www.ema.europa.eu/en/medicines/download-medicine-data) of authorised, refused and withdrawn drug/indication pairs we aim at predicting market authorisation of new pharmaceutical candidates. Given the simple user input of INN (international nonproprietary name), therapeutic area and [orphan medicine](https://en.wikipedia.org/wiki/Orphan_drug) status we aggregate additional features from the [ClinicalTrials.gov](https://clinicaltrials.gov/api/) and [PubMed](https://www.ncbi.nlm.nih.gov/home/develop/api/) APIs. Apart from numerical and one categorial features, we use [Tf-idf-vectoriced](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting) abstracts to train a [Random Forest Classifier](https://scikit-learn.org/stable/modules/ensemble.html#random-forests).

▶ [Live demo](https://pharmapredict.herokuapp.com/)

![](demo.gif)

## Data
### Sources
[EMA](https://www.ema.europa.eu/en/medicines/download-medicine-data)

[PubMed](https://pubmed.ncbi.nlm.nih.gov/)

[ClinicalTrials.gov](https://clinicaltrials.gov/)

### Construction of dataset
From the EMA Excel sheet (see above), colulmns 'Medicine name', 'Therapeutic area', 'INN', 'Authorisation status', 'Generic, 'Biosimilar', 'Orphan medicine' and 'First published' were selected. The file was filtered to only show entries with Authorisation status 'refused' or 'authorised'.
Entries in 'Therapeutic area' were manually transformed to represent multiple therapeutic areas separated by comma.
For each row, searches in the PubMed and ClinicalTrials API were conducted using the following formula: (therapeutic_area_1 OR therapeutic_area_2 etc) AND (INN) AND (date < 'First published'). From these search queries, the remaining columns were filled.
