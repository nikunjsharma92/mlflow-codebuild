import pickle
import sklearn

class MLFlowServer:
	def __init__(self):
		self._model = pickle.load(open('./artifact_downloads/model.pkl', 'rb'))


	def input_fn(self, X):
		try:
			import artifact_downloads.hooks as hooks	
		except Exception as e:
			# raise custom exceptions
			return X
		
		X = hooks.input_hook(X)
		return X

	def predict_fn(self, X):
		try:
			X = self.input_fn(X)
		except Exception as e:
			print("No input hook found")
			
		# predict from model
		Y = self._model.predict(X)
		return Y

		
