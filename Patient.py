import json

class Patient():
	problems = []
	allergies = []
	socialHistory = []
	vitalSigns = []
	medications = []
	results = []
	procedures = []

	postalCode = ""
	gender = ""
	dateOfBirth = ""
	race = ""
	ethnicity = ""


	def __init__(self):
		self.name = 'N/A'

	def jsonify(self):
		jsonFile = {
			"patientInformation": {
				"postalCode": self.postalCode,
				"gender": self.gender,
				"dateOfBirth": self.dateOfBirth,
				"race": self.race,
				"ethnicity": self.ethnicity,
			},
			"problems": self.jsonifyArray(self.problems),
			"allergies": self.jsonifyArray(self.allergies),
			"socialHistory": self.jsonifyArray(self.socialHistory),
			"vitalSigns": self.jsonifyArray(self.vitalSigns),
			"medications": self.jsonifyArray(self.medications),
			"results": self.jsonifyArray(self.results),
			"procedures": self.jsonifyArray(self.procedures)
		}

		return json.dumps(jsonFile, indent=4, sort_keys=True)

	def jsonifyArray(self, jsonArray):
		result = []
		for jsonObject in jsonArray:
			result.append(jsonObject.jsonify())
		return result
