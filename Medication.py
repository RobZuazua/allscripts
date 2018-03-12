class Medication():

	date = ""
	
	def __init__(self):
		self.name = 'N/A'

	def jsonify(self):
		jsonFile = {
			"date": self.date,
			"dose": self.dose,
			"timeframe": self.timeFrame,
			"medication": self.medication
		}
		return jsonFile