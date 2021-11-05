import streamlit as st

import timeit
import pandas as pd
import matplotlib.pyplot as plt

from tpot import TPOTClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits, load_iris
from sklearn import metrics
from stqdm import stqdm


@st.cache
def load_data(dataset):
	"""Load data"""
	ds = ''
	if dataset == 'digits':
		ds = load_digits()
		df = load_digits(as_frame=True)
	if dataset == 'iris':
		ds = load_iris()
		df = load_iris(as_frame=True)
	X_train, X_test, y_train, y_test = train_test_split(ds.data, ds.target, train_size=train_size, test_size=test_size, random_state=random_state)
	return X_train, X_test, y_train, y_test, df['frame']

if __name__ == "__main__":

	# Set title and description
	st.title("AutoML Pipeline Optimization Sandbox")
	st.write("Experiment with using open source automated machine learning tool TPOT for building fully-automated prediction pipelines")

	# Create sidebar
	sidebar = st.sidebar
	dataset = sidebar.selectbox('Dataset', ['iris','digits'])
	train_display = sidebar.checkbox('Display training data', value=True)
	search_iters = sidebar.slider('Number of search iterations', min_value=1, max_value=5)
	generations = sidebar.slider('Number of generations', min_value=1, max_value=10)
	population_size = sidebar.select_slider('Population size', options=[10,20,30,40,50,60,70,80,90,100])

	random_state = 42
	train_size = 0.75
	test_size = 1.0 - train_size
	checkpoint_folder = './tpot_checkpoints'
	output_folder = './tpot_output'
	verbosity = 0
	n_jobs = -1
	times = []
	best_pipes = []
	scores = []

	# Load (and display?) data
	X_train, X_test, y_train, y_test, df = load_data(dataset)
	if train_display:
		st.write(df)

	# Define scoring metric and model evaluation method
	scoring = 'accuracy'
	cv = ('stratified k-fold cross-validation',
			StratifiedKFold(n_splits=10,
			                shuffle=True,
			                random_state=random_state))

	# Define search
	tpot = TPOTClassifier(cv=cv[1],
			      scoring=scoring,
			      verbosity=verbosity,
			      random_state=random_state,
			      n_jobs=n_jobs,
		   	      generations=generations,
			      population_size=population_size,
			      periodic_checkpoint_folder=checkpoint_folder)

	# Pipeline optimization iterations
	with st.spinner(text='Pipeline optimization in progress'):
		for i in stqdm(range(search_iters)):
			start_time = timeit.default_timer()
			tpot.fit(X_train, y_train)
			elapsed = timeit.default_timer() - start_time
			score = tpot.score(X_test, y_test)
			best_pipes.append(tpot.fitted_pipeline_)
			st.write(f'\n__Pipeline optimization iteration: {i}__\n')
			st.write(f'* Elapsed time: {elapsed} seconds')
			st.write(f'* Pipeline score on test data: {score}')
			tpot.export(f'{output_folder}/tpot_{dataset}_pipeline_{i}.py')

	# check if pipelines are the same
	result = True
	first_pipe = str(best_pipes[0])
	for pipe in best_pipes:
		if first_pipe != str(pipe):
			result = False
	if (result):
		st.write("\n__All best pipelines were the same:__\n")
		st.write(best_pipes[0])
	else:
		st.write('\nBest pipelines:\n')
		st.write(*best_pipes, sep='\n\n')

	st.write('__Saved to file:__\n')
	st.write(f'```{output_folder}/tpot_{dataset}_pipeline_{i}.py```')
	st.success("Pipeline optimization complete!")

	# Output contents of best pipe file
	with open (f'{output_folder}/tpot_{dataset}_pipeline_{i}.py', 'r') as best_file:
		code = best_file.read()
	st.write(f'```{code}```')