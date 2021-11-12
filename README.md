

## Description

This a Library System


## Python version

Please use Python version 3.6 or newer versions. 
Otherwise, you will receive an exception
```python
Exception('Requires python 3.6 and above')
```

## Installation

### 0. open the correspending folder via CLI

### 1. Virtual environment set up and run it

**Windows**
```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
```
**MacOS**
```shell
$ python3 -m venv venv
$ source venv/bin/activate
```
###  2. Install dependencies via requirment.txt

```shell 
$ pip install -r requirements.txt
```
When using PyCharm for requirements installation, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

### 3. Run 
From the project directory, and within the activated virtual environment
```shell 
$ flask run
```

#### 4. Testing
From the project directory, and within the activated virtual environment
**Windows**
```shell 
$ python –m pytest –v database_tests
```
**MacOS**
```shell 
$ python –m pytest –v database_tests
```


## Data sources 

The data in the excerpt files were downloaded from (Comic & Graphic):
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

On this webpage, you can find more books and authors in the same file format as in our excerpt, for example for different book genres. 
These might be useful to extend your web application with more functionality.

We would like to acknowledge the authors of these papers for collecting the datasets by extracting them from Goodreads:

*Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.*

*Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19.*
