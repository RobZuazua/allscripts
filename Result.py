class Result():

	date = ""
	
	def __init__(self):
		self.name = 'N/A'

	def jsonify(self):
		jsonFile = {
			"value": self.value,
			"code": self.code,
			"unit": self.unit,
			"displayName" :self.displayName
		}
		return jsonFile