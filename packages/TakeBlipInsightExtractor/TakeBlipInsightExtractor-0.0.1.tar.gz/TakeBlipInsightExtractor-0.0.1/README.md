# Insight Extractor Cloud
_Data & Analytics Research_

## Overview

Here is presented these content:

* [Intro](#intro)
* [Configure](#configure)
* [Run](#run)


## Intro

The Insight Extractor Cloud (IE Cloud) offers a way to analyze huge volumes of textual data in order to identify, cluster and detail subjects. 
This project achieves this results by way of applying a proprietary Named Entity Recognition (NER) algorithm followed by a clustering algorithm. 
The IE Cloud also allows any person to use this tool without having too many computational resources available to themselves.

IE Cloud outputs four types of files:

- **Wordcloud**: It's an image file containing a wordcloud describing the most frequent subjects on the text. The colours represent the groups of similar subjects.
- **Wordtree**: It's an html file which contains the graphic relationship between the subjects and the examples of uses in sentences. It's an interactive graphic where the user can navigate along the tree.
- **Hierarchy**: It's a json file which contains the hierarchical relationship between subjects.
- **Table**: It's a csv file containing the following columns:

       
        Message                   |  Entities                                                                                    | Groups     | Structured Message
        sobre cobranca inexistente|[{'value': 'cobrança', 'lowercase_value': 'cobrança', 'postags': 'SUBS', 'type': 'financial'}]|['cobrança']|sobre cobrança inexistente


## Configure

Here are shown recommended practices to configure project on local.

### Virtual environment

This step can be done with commands.

#### On commands

It is recommended to use virtual environment. To Create a virtual environment:

```
conda env create -f conda_env/insightextractor.yml
```

To activate virtual enviroment:

```
conda activate insightextractor3.6
```

To exit virtual environment:

```
conda deactivate
```

In order to run IE Cloud locally the three used models need to be on the project folder. 

For the Embedding model the files needed are:
- *vectors_ngrams.npy
- *vectors_vocab.npy
- *vectors.npy
- *.kv

For the NER model the files needed are:
- *.pkl (for the model)
- *.pkl (for the vocab)

For the PosTagging model the files needed are:
- *.pkl (for the model)
- *.pkl (for the vocab)


## Run

The file to be analyzed needs to be a .csv with one column with the messages.

To test IE Cloud locally on the command line:

```
python insight_extractor.py --node_messages_examples 100 --similarity_threshold 0.65 --percentage_threshold 0.9 --batch_size 512 --embedding_path *.kv --postagging_model_path *.pkl  --postagging_label_path *.pkl --ner_model_path *.pkl --ner_label_path *.pkl --file YOUR_DATA.csv --user_email YOUR_EMAIL@take.net --bot_name BOT_NAME --separator "|" --chunk_size 16224
```

### Parameters

The following parameters need to be set by the user on the command line:
- **embedding_path**: path to the embedding model, the file should end with .kv;
- **postagging_model_path**: path to the postagging model, the file should end with .pkl;
- **postagging_label_path**: path to the postagging label file, the file should end with .pkl;
- **ner_model_path**: path to the ner model, the file should end with .pkl;
- **ner_label_path**: path to the ner label file, the file should end with .pkl;
- **file**: path to the csv file the user wants to analyze;
- **user_email**: user's Take Blip email where they want to receive the analysis;
- **bot_name**: bot ID.


The following parameters have default settings, but can be customized by the user;
- **node_messages_examples**: it is an int representing the number of examples outputed for each subject on the Wordtree file. The default value is 100;
- **similarity_threshold**: it is a float representing the similarity threshold between the subject groups. The default value is 0.65, we recommend that this parameter not be modified;
- **percentage_threshold**: it is a float representing the frequency percentile of subject from which they are not removed from the analysis. The default value is 0.9;
- **batch_size**: it is an int representing the batch size. The default value is 50;
- **chunk_size**: it is an int representing chunk file size for upload in storaged. The default value is 1024;
- **separator**: it is a str for the csv file delimiter character. The default value is '|'.
          

       
    