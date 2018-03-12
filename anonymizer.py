from bs4 import BeautifulSoup
import io
from Patient import Patient
from Problem import Problem
from Allergy import Allergy
from SocialHistory import SocialHistory
from VitalSign import VitalSign
from Medication import Medication
from Result import Result
from Procedure import Procedure

# Beautiful Soup 4 prepare and parse xml
xml = open("./ccda.xml", "r")
contents = xml.read()
parsedXML = BeautifulSoup(contents, 'xml')

# Create Patient object and store obfuscated details
patientObj = Patient()
patientObj.postalCode = parsedXML.find_all('postalCode')[0].get_text()
patientObj.gender = parsedXML.find_all('administrativeGenderCode')[0].attrs["code"]
patientObj.dateOfBirth = parsedXML.find_all('birthTime')[0].attrs["value"]
patientObj.race = parsedXML.find_all('raceCode')[0].attrs["code"]
patientObj.ethnicity = parsedXML.find_all('ethnicGroupCode')[0].attrs["code"]

# Break XML into the main components
parsedXMLBody = parsedXML.ClinicalDocument.component.structuredBody
parsedXMLArray = parsedXMLBody.find_all('component',recursive=False)

parsedXMLProblems = parsedXMLArray[0].section.find_all('entry')
parsedXMLAllergies = parsedXMLArray[1].section.find_all('entry')
parsedXMLSocialHistory = parsedXMLArray[2].section.find_all('entry')
parsedXMLVitalSigns = parsedXMLArray[3].section.find_all('entry')
parsedXMLMedications = parsedXMLArray[4].section.find_all('entry')
parsedXMLResults = parsedXMLArray[5].section.find_all('entry')
parsedXMLProcedures = parsedXMLArray[6].section.find_all('entry')
 
# Problems
for problem in parsedXMLProblems:
	patientProblem = Problem()
	patientProblem.date = problem.act.effectiveTime.low.attrs["value"]
	patientProblem.code = problem.act.entryRelationship.observation.value.attrs["code"]
	patientProblem.displayName = problem.act.entryRelationship.observation.value.attrs["displayName"]
	
	patientObj.problems.append(patientProblem)

# Allergies
for allergy in parsedXMLAllergies:
	patientAllergy = Allergy()
	patientAllergy.date = allergy.act.effectiveTime.low.attrs["value"]
	patientAllergy.code = allergy.act.entryRelationship.observation.value.attrs["code"]
	patientAllergy.displayName = allergy.act.entryRelationship.observation.value.attrs["displayName"]

	patientObj.allergies.append(patientAllergy)

# Social History
for history in parsedXMLSocialHistory:
	patientHistory = SocialHistory()
	if history.observation.effectiveTime.low.attrs["nullFlavor"] != "UNK":
		patientHistory.date = history.observation.effectiveTime.low.attrs["value"]
	
	patientHistory.code = history.observation.value.attrs["code"]
	patientHistory.displayName = history.observation.value.attrs["displayName"]

	patientObj.socialHistory.append(patientHistory)

# Vital Signs
vitalSigns = []
for vitalSign in parsedXMLVitalSigns:
	vitalSigns = vitalSigns + vitalSign.find_all("component")
for vitalSign in vitalSigns:
	patientVitalSign = VitalSign()
	patientVitalSign.date = vitalSign.observation.effectiveTime.attrs["value"]
	patientVitalSign.code = vitalSign.code.attrs["code"]
	patientVitalSign.displayName = vitalSign.code.attrs["displayName"]

	patientObj.vitalSigns.append(patientVitalSign)


# Medications
for medication in parsedXMLMedications:
	patientMedication = Medication()

	# has effectivetime here a lowercase "t"??
	patientMedication.date = medication.substanceadministration.find_all("effectivetime")[0].low.attrs["value"]
	patientMedication.timeFrame = {
		"time": medication.substanceadministration.find_all("effectivetime")[1].period.attrs["value"],
		"unit": medication.substanceadministration.find_all("effectivetime")[1].period.attrs["unit"]
	}

	patientMedication.dose = {
		"value": medication.substanceadministration.dosequantity.attrs["value"],
		"unit": medication.substanceadministration.dosequantity.attrs["unit"]
	}
	patientMedication.medication = {
		"code": medication.substanceadministration.consumable.manufacturedproduct.manufacturedmaterial.code.attrs["code"],
		"displayName": medication.substanceadministration.consumable.manufacturedproduct.manufacturedmaterial.code.attrs["displayname"]
	}

	patientObj.medications.append(patientMedication)


# Results
for result in parsedXMLResults:
	parsedXMLResultsComponents = result.organizer.find_all("component", recursive=False)

	for component in parsedXMLResultsComponents:
		patientResult = Result()
		patientResult.code = component.observation.code.attrs["code"]
		patientResult.displayName = component.observation.code.attrs["displayName"]
		patientResult.value = component.observation.value.attrs["value"]
		patientResult.unit = component.observation.value.attrs["unit"]
		patientObj.results.append(patientResult)

# Procedures


print(patientObj.jsonify())