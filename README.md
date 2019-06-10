## Language detector
This is an implementation of a software which can detect language of texts. 
It's designed for detecting the language in longer texts such as scientific-papers, which can come in *.txt
or *.pdf format. The language detector introduces a custom algorithm which is referred as for detecting the "spatial language identificator (sli) comparison".
It aims to use as less external libraries for the classification as possible. 
### Program overview 
![Overview of workflow of langdet and structure of sli](/docs/graphics_langdet/workflow_langdet.png)


### Test Results 
There we're 12 documents checked for testing. The document pool exists of scientific papers, wikipedia-articles and 
languages. In the pool there we're 3 english, 3 german, 3 french, 2 thai and 1 spanish document. These documents are not provided here because of licensing. Sample result output for a scientific paper
looks like this. All of these documents were classified correctly. The system was trained with input data in the same languages. 

The first document was a scientific paper on sentiment-analysis, which is availible [here](https://www.aclweb.org/anthology/D13-1170): 
Result output can be seen below. 

```
Results______________________________________________________
Input:     io_data/langdet/document_rsocher.pdf
Det. lang: en                       
_____________________________________________________________
language   distance                  likeliness               
en         6375.422232185437         68.11193438031768        
fr         7032.559338922403         64.82511973218834        
sp         7586.859986309798         62.05266407777083        
de         7835.992906497068         60.8065714085122         
th         19993.129430373243        0.0            
```

### Pro's and Con's 
Pro's: 
- learning language datasets is fast, under 3 minutes for 6 languages
- the saved sli's for identification take nearly no disk space (for 6 languages it's below 85 kb)
- making comparison is fast and doesn't take much cpu to process
- learn dataset is availible freely in nearly any language (bible)
- detection with test dataset of 12 documents in different languages was 100% accurate 
- simple algorithm, which could be easily adapted in other programming languages and even used on microcontrollers

Con's: 
- much text required compared to dictionary approach 
- no measurement that a text isn't of any of the supported languages

### Usage 
- Adapt read in file config in "configurations/language_detector.conf". 
- Execute 'langedet_create_dataset.py' for creating some comparison sli's. 
- Execute 'langdet_check_language.py' for language identification of your specified documents, results appear in stdout

IDE for development was PyChar Community Edition by Jetbrains

### Possible future improvements  
- instead of using least mean square comparison, train a neural classificator for distinquishing input texts. The training could be with chapter wise info from the training data 
- pre-filter non-text info from pdf-data 
- filter the charset used for comparison in the sli-objects
- provide more language support, by learning in more bibles 
- make an adaptive web-interface, which allows to add correctly classified sli's to the comparison dataset
- create an n-gram based sli, to take character follow up sequences to account 
- take one international version of the bible in many languages as learn in dataset
- find treshold or algorithm to detect texts which are not any of the supported languages 
- find alternative for tike webservice for pdf-reading 


### References used

- book graphic in diagram by Abilngeorge and under CC-License  [here](https://de.wikipedia.org/wiki/Datei:Indian_Election_Symbol_Book.svg)
- [tika library](https://github.com/chrismattmann/tika-python) is used to get *.pdf-file content. The library contacts a web service for that
- for creating documentation diagrams [yED](https://www.yworks.com/products/yed) was used 
- bibles for learning in can be obtained from [ebible.org](https://ebible.org/find/)
