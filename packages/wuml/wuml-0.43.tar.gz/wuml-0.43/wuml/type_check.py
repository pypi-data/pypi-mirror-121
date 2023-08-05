
import numpy as np
import torch
import pandas as pd
from torch.autograd import Variable


def ensure_DataFrame(data):
	if type(data).__name__ == 'ndarray': 
		df = pd.DataFrame(data)
	elif type(data).__name__ == 'wData': 
		df = data.df
	elif type(data).__name__ == 'DataFrame': 
		df = data
	elif type(data).__name__ == 'Tensor': 
		X = data.detach().cpu().numpy()
		df = pd.DataFrame(X)

	return df



def ensure_numpy(data, rounding=None):
	if type(data).__name__ == 'ndarray': 
		if len(data.shape) == 1:
			X = np.atleast_2d(data).T
		else:
			X = data
	elif type(data).__name__ == 'wData': 
		X = data.df.values
	elif type(data).__name__ == 'DataFrame': 
		X = data.values
	elif type(data).__name__ == 'Tensor': 
		X = data.detach().cpu().numpy()
	elif np.isscalar(data):
		X = np.array([[data]])

	if rounding is not None: X = np.round(X, rounding)
	return X


def ensure_tensor(data, dataType=torch.FloatTensor):
	if torch.cuda.is_available(): 
		device = 'cuda'
	else: self.device = 'cpu'

	if type(data).__name__ == 'ndarray': 
		x = torch.from_numpy(data)
		x = Variable(x.type(dataType), requires_grad=False)
		X = x.to(device, non_blocking=True )
	elif type(data).__name__ == 'wData': 
		X = data.get_data_as('Tensor')
	elif type(data).__name__ == 'DataFrame': 
		X = data.values
	elif np.isscalar(data):
		X = np.array([[data]])
	elif type(data).__name__ == 'Tensor': 
		x = Variable(data.type(dataType), requires_grad=False)
		X = x.to(device, non_blocking=True )
	else:
		raise ValueError('Unknown dataType %s'%type(data).__name__)

	return X





