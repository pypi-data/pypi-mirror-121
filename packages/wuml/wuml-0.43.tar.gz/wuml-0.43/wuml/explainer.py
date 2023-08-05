

import shap		#pip install shap
import wuml

class explainer():
	def __init__(self, data, explainer_algorithm='shap', link='identity',
						model=None, 										# Use this if you have your own model, input/output should be nparray
						loss='mse',  										#use these options if you use a default regression
						networkStructure=[(100,'relu'),(100,'relu'),(1,'none')], 
						max_epoch=1000, learning_rate=0.001):

		'''
			use link='identity' for regression and link='logit' for classification
		'''

		X = wuml.ensure_numpy(data)

		if explainer_algorithm == 'shap':
			if model is not None:
				self.Explr = shap.KernelExplainer(model, np.zeros(X.shape), link=link)
			else:
				self.bNet = wuml.basicNetwork(loss, data, networkStructure=networkStructure, max_epoch=max_epoch, learning_rate=learning_rate)
				self.bNet.train()
				self.bNet.eval(output_type='ndarray')
				self.Explr = shap.KernelExplainer(self.bNet, X, link=link)		#, l1_reg=False



	def __call__(self, data, nsamples=20):
		X = wuml.ensure_numpy(data)
		return self.Explr.shap_values(X, nsamples=nsamples)



