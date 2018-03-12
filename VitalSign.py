class VitalSign():

	date = ""
	
	def __init__(self):
		self.name = 'N/A'

	def jsonify(self):
		jsonFile = {
			"date": self.date,
			"code": self.code,
			"displayName": self.displayName
		}
		return jsonFile