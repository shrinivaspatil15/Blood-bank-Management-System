import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

def create_bar(x_data, y_data, title, x_label, y_label):
	# fig, ax = plt.subplots()
	fig=Figure()
	ax=fig.add_subplot(1,1,1)
	ax.bar(x_data, y_data, color='rgbymc')
	ax.set_title(title, fontsize=18)
	ax.set_xlabel(x_label, fontsize=14)
	ax.set_ylabel(y_label, fontsize=14)
	ax.set_xticks(np.arange(len(x_data)))
	ax.set_xticklabels(x_data)
	ax.set_yticks(np.arange(np.max(y_data) + 3))
	ax.set_yticklabels(np.arange(np.max(y_data) + 3))
	return fig

def create_pie(data, labels):
	fig = plt.figure(figsize=(5, 3))
	plt.pie(data,labels=labels, shadow=True)
	return fig
