import argparse
from pathlib import Path
from typing import List, Any

import numpy as np
from lime.lime_text import LimeTextExplainer
import sklearn.pipeline
import scipy.stats
import spacy


METHODS = {
    'textblob': {
        'class': "TextBlobExplainer",
        'file': None,
        'name': "TextBlob",
        'lowercase': False,
    },
    'vader': {
        'class': "VaderExplainer",
        'file': None,
        'name': "VADER",
        'lowercase': False,
    },
    'logistic': {
        'class': "LogisticExplainer",
        'file': "data/sst/sst_train.txt",
        'name': "Logistic Regression",
        'lowercase': False,
    },
    'svm': {
        'class': "SVMExplainer",
        'file': "data/sst/sst_train.txt",
        'name': "Support Vector Machine",
        'lowercase': False,
    },
    'fasttext': {
        'class': "FastTextExplainer",
        'file': "models/fasttext/sst5_hyperopt.ftz",
        'name': "FastText",
        'lowercase': True,
    },
}


def tokenizer(text: str) -> str:
    "Tokenize input string using a spaCy pipeline"
    nlp = spacy.blank('en')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))  # Very basic NLP pipeline in spaCy
    doc = nlp(text)
    tokenized_text = ' '.join(token.text for token in doc)
    return tokenized_text


def explainer_class(method: str, filename: str) -> Any:
    "Instantiate class using its string name"
    classname = METHODS[method]['class']
    class_ = globals()[classname]
    return class_(filename)


class TextBlobExplainer:
    """Class to explain classification results of TextBlob.
       Although Textblob overall polarity scores are in the range [-1.0, 1.0], we `simulate`
       the probabilities that the model predicts using 5 equally-sized bins in this interval.
       and using a normal distribution to artificially create class probabilities.

       For example:
       If TextBlob predicts a float sentiment score of -0.62, we offset this to be within
       the range [0, 1] by adding 1 and then halving the score. This translates to an offset
       score of 0.19. This is then converted to an integer-scaled class prediction of 1,
       assuming equally-sized bins for 5 classes.
       We take this value and generate a normal distribution PDF with exactly 5 values.
       The PDF is used as a simulated probability of classes that we feed to the LIME explainer.
    """
    def __init__(self, model_file: str = None) -> None:
        self.classes = np.array([1, 2, 3, 4, 5])

    def score(self, text: str) -> float:
        # pip install textblob
        from textblob import TextBlob
        return TextBlob(text).sentiment.polarity

    def predict(self, texts: List[str]) -> np.array([float, ...]):
        probs = []
        for text in texts:
            # First, offset the float score from the range [-1, 1] to a range [0, 1]
            offset = (self.score(text) + 1) / 2.
            # Convert offset float score in [0, 1] to an integer value in the range [1, 5]
            binned = np.digitize(5 * offset, self.classes) + 1
            # Similate probabilities of each class based on a normal distribution
            simulated_probs = scipy.stats.norm.pdf(self.classes, binned, scale=0.5)
            probs.append(simulated_probs)
        return np.array(probs)


class VaderExplainer:
    """Class to explain classification results of Vader.
       Although VADER compound scores are in the range [-1.0, 1.0], we `simulate` the 
       probabilities that the model predicts using 5 equally-sized bins in this interval.
       and using a normal distribution to artificially create class probabilities.

       For example:
       If Vader predicts a float sentiment score of 0.6834, this translates to an
       integer-scaled class prediction of 4, assuming equally-sized bins for 5 classes.
       We take this value and generate a normal distribution PDF with exactly 5 values.
       The PDF is used as a simulated probability of classes that we feed to the LIME explainer.
    """
    def __init__(self, model_file: str = None) -> None:
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
        except:
            import nltk
            nltk.download('vader_lexicon')
        self.vader = SentimentIntensityAnalyzer()
        self.classes = np.array([1, 2, 3, 4, 5])

    def score(self, text: str) -> float:
        return self.vader.polarity_scores(text)['compound']

    def predict(self, texts: List[str]) -> np.array([float, ...]):
        probs = []
        for text in texts:
            # First, offset the float score from the range [-1, 1] to a range [0, 1]
            offset = (self.score(text) + 1) / 2.
            # Convert float score in [0, 1] to an integer value in the range [1, 5]
            binned = np.digitize(5 * offset, self.classes) + 1
            # Similate probabilities of each class based on a normal distribution
            simulated_probs = scipy.stats.norm.pdf(self.classes, binned, scale=0.5)
            probs.append(simulated_probs)
        return np.array(probs)


class LogisticExplainer:
    """Class to explain classification results of a scikit-learn
       Logistic Regression Pipeline. The model is trained within this class.
    """
    def __init__(self, path_to_train_data: str) -> None:
        "Input training data path for training Logistic Regression classifier"
        import pandas as pd
        # Read in training data set
        self.train_df = pd.read_csv(path_to_train_data, sep='\t', header=None, names=["truth", "text"])
        self.train_df['truth'] = self.train_df['truth'].str.replace('__label__', '')
        # Categorical data type for truth labels
        self.train_df['truth'] = self.train_df['truth'].astype(int).astype('category')

    def train(self) -> sklearn.pipeline.Pipeline:
        "Create sklearn logistic regression model pipeline"
        from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        pipeline = Pipeline(
            [
                ('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression(
                    solver='newton-cg',
                    multi_class='multinomial',
                    random_state=42,
                    max_iter=100,
                )),
            ]
        )
        # Train model
        classifier = pipeline.fit(self.train_df['text'], self.train_df['truth'])
        return classifier

    def predict(self, texts: List[str]) -> np.array([float, ...]):
        """Generate an array of predicted scores (probabilities) from sklearn
        Logistic Regression Pipeline."""
        classifier = self.train()
        probs = classifier.predict_proba(texts)
        return probs


class SVMExplainer:
    """Class to explain classification results of a scikit-learn linear Support Vector Machine
       (SVM) Pipeline. The model is trained within this class.
    """
    def __init__(self, path_to_train_data: str) -> None:
        "Input training data path for training Logistic Regression classifier"
        import pandas as pd
        # Read in training data set
        self.train_df = pd.read_csv(path_to_train_data, sep='\t', header=None, names=["truth", "text"])
        self.train_df['truth'] = self.train_df['truth'].str.replace('__label__', '')
        # Categorical data type for truth labels
        self.train_df['truth'] = self.train_df['truth'].astype(int).astype('category')

    def train(self) -> sklearn.pipeline.Pipeline:
        "Create sklearn logistic regression model pipeline"
        from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
        from sklearn.linear_model import SGDClassifier
        from sklearn.pipeline import Pipeline
        pipeline = Pipeline(
            [
                ('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(
                    loss='modified_huber',
                    penalty='l2',
                    alpha=1e-3,
                    random_state=42,
                    max_iter=100,
                    tol=None,
                )),
            ]
        )
        # Train model
        classifier = pipeline.fit(self.train_df['text'], self.train_df['truth'])
        return classifier

    def predict(self, texts: List[str]) -> np.array([float, ...]):
        """Generate an array of predicted scores (probabilities) from sklearn
        Logistic Regression Pipeline."""
        classifier = self.train()
        probs = classifier.predict_proba(texts)
        return probs


class FastTextExplainer:
    """Class to explain classification results of FastText.
       Assumes that we already have a trained FastText model with which to make predictions.
    """
    def __init__(self, path_to_model: str) -> None:
        "Input fastText trained sentiment model"
        import fasttext
        self.classifier = fasttext.load_model(path_to_model)

    def predict(self, texts: List[str]) -> np.array([float, ...]):
        "Generate an array of predicted scores using the FastText"
        labels, probs = self.classifier.predict(texts, 5)

        # For each prediction, sort the probability scores in the same order for all texts
        result = []
        for label, prob, text in zip(labels, probs, texts):
            order = np.argsort(np.array(label))
            result.append(prob[order])
        return np.array(result)


def explainer(method: str,
              path_to_file: str,
              text: str,
              lowercase:bool,
              num_samples: int) -> LimeTextExplainer:
    """Run LIME explainer on provided classifier"""

    model = explainer_class(method, path_to_file)
    predictor = model.predict
    # Lower case the input text if requested (for certain classifiers)
    if lowercase:
        text = text.lower()

    # Create a LimeTextExplainer
    explainer = LimeTextExplainer(
        # Specify split option
        split_expression=lambda x: x.split(),
        # Our classifer uses trigrams or contextual ordering to classify text
        # Hence, order matters, and we cannot use bag of words.
        bow=False,
        # Specify class names for this case
        class_names=[1, 2, 3, 4, 5]
    )

    # Make a prediction and explain it:
    exp = explainer.explain_instance(
        text,
        classifier_fn=predictor,
        top_labels=1,
        num_features=20,
        num_samples=num_samples,
    )
    return exp


def main(samples: List[str]) -> None:
    # Get list of available methods:
    method_list = [method for method in METHODS.keys()]
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', type=str, nargs='+', help="Enter one or more methods \
                        (Choose from following: {})".format(", ".join(method_list)),
                        required=True)
    parser.add_argument('-n', '--num_samples', type=int, help="Number of samples for explainer \
                        instance", default=1000)
    args = parser.parse_args()

    for method in args.method:
        if method not in METHODS.keys():
            parser.error("Please choose from the below existing methods! \n{}".format(", ".join(method_list)))
        path_to_file = METHODS[method]['file']
        ENABLE_LOWER_CASE = METHODS[method]['lowercase']
        # Run explainer function
        print("Method: {}".format(method.upper()))
        for i, text in enumerate(samples):
            text = tokenizer(text)  # Tokenize text using spaCy before explaining
            print("Generating LIME explanation for example {}: `{}`".format(i+1, text))
            exp = explainer(method, path_to_file, text, ENABLE_LOWER_CASE, args.num_samples)
            # Output to HTML
            output_filename = Path(__file__).parent / "{}-explanation-{}.html".format(i+1, method)
            exp.save_to_file(output_filename)


if __name__ == "__main__":
    # Evaluation text
    samples = [
        "It 's not horrible , just horribly mediocre .",
        "The cast is uniformly excellent ... but the film itself is merely mildly charming .",
    ]
    main(samples)
