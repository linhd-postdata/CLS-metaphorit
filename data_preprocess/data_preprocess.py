import pandas as pd

from datasets import Dataset
from datasets import DatasetDict

from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer


def corpus_to_hf_dataset(dataframe:pd.DataFrame, tokenizer: AutoTokenizer) -> Dataset:
    """
    Converts the corpus to a HuggingFace DatasetDict and tokenizes the sentences.

    Args:
        dataframe (pd.DataFrame): The corpus to be converted and tokenized.
        tokenizer (HF tokenizer): The HuggingFace tokenizer to be used for tokenization.

    Returns:
        DatasetDict: The tokenized corpus in the form of a HuggingFace DatasetDict.
    """
    dataset = DatasetDict()
    df = dataframe.copy().sample(frac=1, random_state=42)
    
    le = LabelEncoder()
    df.labels = le.fit_transform(df.labels)

    dataset['train'] = Dataset.from_pandas(df[df.split=='train'])
    dataset['validation'] = Dataset.from_pandas(df[df.split=='dev'])
    dataset['test'] = Dataset.from_pandas(df[df.split == 'test'])

    remove_columns = [x for x in df.columns.to_list() if x!='labels'] + ['__index_level_0__']
    df = dataset.map(lambda x: tokenizer(x['Sentence'], truncation=True),
                     batched=True, 
                     remove_columns=remove_columns)
    return df