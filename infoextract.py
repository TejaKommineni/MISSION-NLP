'''
Created on Nov 3, 2017

@author: tejak
'''
import sys,re,os
import nltk
from nltk.corpus import wordnet
from nltk.tag import StanfordNERTagger 
import inflect
import spacy
from spacy.symbols import nsubj,nsubjpass,pobj,dobj,VERB

#os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk1.8.0_131/bin'

class EventExtraction:
        
        
    def event_extraction(self):
        r = open(self.filename,"r")
        prev = ""   
        for line in r:
            if ("DEV-MUC3-" in line) or ("TST1-MUC3-" in line) or ("TST2-MUC4-" in line):            
                if prev != "":
                   self.f.write("ID:             "+self.ID.split("(")[0] +"\n")
		   #print(prev)		   
		   self.evaluate_incident(prev)
	           self.evaluate_weapon(prev)
        	   self.evaluate_prep_indiv(prev)
	           self.evaluate_prep_org(prev)
	       	   self.evaluate_target(prev)
		   self.evaluate_victim(prev)                 
		   self.f.write("\n")
                self.ID = line.strip()
                prev = ""
            else:
                prev = prev + " " + line.strip()
        
        self.f.write("ID:             "+self.ID.split("(")[0]+"\n")
        self.evaluate_incident(prev)
	self.evaluate_weapon(prev)
	self.evaluate_prep_indiv(prev)
	self.evaluate_prep_org(prev)
	self.evaluate_target(prev)
	self.evaluate_victim(prev)   
	self.f.write("\n")
        
    
    def evaluate_incident(self,prev):
	prev = prev.lower()
	event = {}
	dict_keywords = {'fires':5, 'bombardment':5,  'arson(?=\s)': 5,  'set\s+ablaze': 15, 'set\s+aflame': 15, 'set\s+fire\s+to': 15, 'houses\s+on\s+fire': 20, 'arson': 20,  'places\s+burned': 20, 'incendiary':20, 'buildings\s+on\s+fire': 20, 'burning': 20}
	event['arson'] = self.incident_value(prev,dict_keywords)
	
	dict_keywords =  { '(?<=\s)massacre': 5, '(?<=\s)slaughter': 5, '(?<=\s)attack': 5, '(?<=\s)annihilation': 5, '(?<=\s)firing': 5, '(?<=\s)murder': 5, '(?<=\s)shot': 5,  '(?<=\s)shoot': 10, '(?<=\s)streak': 10,'(?<=\s)ARTILLERY\s+FIRE': 10, '(?<=\s)shoot\-out': 10, '(?<=\s)slaughter': 10,  '(?<=\s)fired\s+rocket': 10, '(?<=\s)assassinat': 10, '(?<=\s)liquidate': 10, '(?<=\s)machine gun\s+attack': 15, '(?<=\s)mortar': 15,  '(?<=\s)firing\s+rockets': 15, '(?<=\s)firing\s+space': 15,  '(?<=\s)launched\s+space': 15,  '(?<=\s)launched\s+rockets': 15, '(?<=\s)molotov': 20}
        event['attack'] =  self.incident_value(prev,dict_keywords)
	
	dict_keywords = {'(?<=\s)bomb': 5, '(?<=\s)projectile': 5, '(?<=\s)explosi': 5, '(?<=\s)bombed rebel': 5, '(?<=\s)gust\-up': 10,  '(?<=\s)blew\-up': 10, '(?<=\s)gust\s+up': 10,  '(?<=\s)blown\s+up': 10, '(?<=\s)blowing\-up': 10, '(?<=\s)gusting\-up': 10, '(?<=\s)ied': 10, '(?<=\s)vbied': 10,  '(?<=\s)explosive\s+device': 10,   '(?<=\s)erupted\s+device': 10, '(?<=\s)explod': 10, '(?<=\s)erupt': 10, '(?<=\s)placed\s+a\s+bomb': 15,'(?<=\s)placed\s+a\s+missile': 15, '(?<=\s)missile\-bomb': 15, '(?<=\s)car\-bomb': 15, '(?<=\s)truck\s+bomb': 15, '(?<=\s)car\s+bomb': 15, '(?<=\s)dynamite': 15, '(?<=\s)grenade': 15,'(?<=\s)detonated': 25}
        event['bombing'] =  self.incident_value(prev,dict_keywords)

	dict_keywords = {'(?<=\s)disappear': 5, '(?<=\s)vanish': 5,  'hostage': 20, 'held\s+detainee': 20, '(?<=\s)kidnap': 20, 'held\s+captive': 20, 'held\s+hostage': 20, '(?<=\s)abduct': 20}	
	event['kidnapping'] =  self.incident_value(prev,dict_keywords)

	dict_keywords = {'(?<=\s)assaulted': 5, '(?<=\s)mugged': 5, '(?<=\s)steal': 5, '(?<=\s)robbery(?=\s)': 5, '(?<=\s)thief': 5, '(?<=\s)stole(?=\s)': 5, '(?<=\s)burglar': 5, '(?<=\s)robbed(?=\s)': 5,  '(?<=\s)burglary': 5}		
	event['robbery'] =  self.incident_value(prev,dict_keywords)

	self.f.write("INCIDENT:      "+ max(event, key=event.get).upper()+"\n")

    def evaluate_weapon(self,prev):	
        flag = False
	#print(self.weapons)
	sentences = nltk.sent_tokenize(prev.upper())
	used_weapons = set()
	for sentence in sentences:
		words = nltk.word_tokenize(sentence)
		for weapon in self.weapons:
            		if weapon.upper() in words:
		                used_weapons.add(weapon)
	first = True	
	for weapon in used_weapons:
	    flag = True
	    if first == True:
		first = False				
		self.f.write("WEAPON:         "+weapon+"\n")
	    else:
		self.f.write("                "+weapon+"\n")
			
        if flag == False:
                self.f.write("WEAPON:         -\n")

    def setup_weapons(self):
        temp = ["125 to 150 grams of tnt", "two devices", "Ayudha katti","powerful rockets", "explosive device","pulwar","dirty bomb", "improvised explosive device", "TNT", "ICBM","knife", "machete", "mortar", "IED","Kilij", "VBIED", "explosive devices", "RPG", "talwar","blowgun", "carbine", "revolver", "shotgun",  "flamethrower", "Khanda","spear", "bayonet", "dagger", "sword", "eight bombs","flamberge", "rockets", "grenades", "dynamite attacks", "bomb set in an ice cream cart",  "missile", "tomahawk cruise missile", "klasksara","bazooka",  "axe", "assault rifle", "harpoon", "gun","claymore", "chemical weapons", "nuclear bomb", "torpedo",  "Remington Model", "baton", "taser", "ordnance",   "terrorist bombs", "several dynamite attacks", ".45 caliber gun",".22 caliber gun", "mine",  "incendiary bomb", ".60 caliber gun","dynamite", "helicopter gunships", "helicopter gunship", ".100 caliber gun","explosive charges", "bullets", "dynamite sticks","heavy caliber weapons","kora", "powerful bomb", "vehicle loaded with explosives", "9-mm weapons","kona", "four bombs",  "machinegun", "a bomb", "at least six bombs", "bombs", "car-bomb", "5 kg of dynamite","submachinegun", "tnt", "bullet", "mortar", "truck", "two dynamite charges", "dynamite charge", "several dynamite sticks", "powerful bombs", "handmade catapults",  "medium-sized bombs", "two bombs", "machinegun"]
	
	self.weapons.extend(temp)

    def evaluate_prep_indiv(self,prev):
        sentences = nltk.sent_tokenize(prev)
        for sentence in sentences:
                doc = self.nlp(sentence.lower().decode('utf8'))                
                #for np in doc.noun_chunks:
                #    print(np.text)

	
	self.f.write("PREP INDV: -\n")
    def evaluate_prep_org(self,prev):
        self.f.write("PREP ORG:  -\n")
    def evaluate_target(self,prev):
	flag = False	
		
	if flag == False:
		self.f.write("TARGET:    -\n")
    def evaluate_victim(self,prev):
	flag = False
        if flag == False:
                self.f.write("VICTIM:    -\n")
	
    def incident_value(self,prev,dict_keywords):
	count = 0	
	for pattern, value in dict_keywords.iteritems():
               count += len(re.findall(pattern, prev, re.IGNORECASE | re.MULTILINE)) * value
	return count

    def is_event(self,prev):
	flag = False
        for word in self.keywords:
                for synonyms in self.synonyms_for_keywords[word]:
                        p = inflect.engine()
                        if synonyms.upper() in prev or p.plural(synonyms).upper() in prev:
				return True
                               
        return False

    def verify_in_keywords(self,keyword,text):
	for synonyms in self.synonyms_for_keywords[keyword]:
            		p = inflect.engine()
                        if synonyms.upper() in text.upper() or p.plural(synonyms).upper() in text.upper():
                         #       print("true")
				return True
	return False

    def setup_key_words(self):
        for word in self.keywords:
          self.synonyms_for_keywords[word] = self.get_synonyms(word)	  
	  #print(self.synonyms_for_keywords[word])
        self.synonyms_for_keywords['attack'].append('murder')
	self.synonyms_for_keywords['attack'].append('killed')
	self.synonyms_for_keywords['bombing'].append('hurled')	
    	self.synonyms_for_keywords['bombing'].append('bomb blast')
	self.synonyms_for_keywords['bombing'].append('explosion')
	temp = ["very powerful explosives", "mortar", "molotov cocktails", "rockets", "mobile armed platforms", "catapults", "charge of dynamite",  "machine-gun", "carbomb", "bomb blast", "bombs", "the bomb", "grenade", "packages of dynamite",  "dynamite charge", "machineguns", "explosives","bomb", "truck bomb","devices", "dynamite", "M4", "AKM", "shank", "PKM", "MP5", "FAL", "dynamite charges", "explosives","17 kg of dynamite"]
	self.weapons.extend(temp)
    
    def get_synonyms(self,word):
        lemmas = []   
        synsets = wordnet.synsets(word) 
	#print(synsets)       
	for sense in synsets:
	        lemmas += [re.sub("_", " ", lemma.name()) for lemma in sense.lemmas()]                  
	return list(set(lemmas))
        
    def __init__(self, filename):
        self.filename = filename
	self.keywords = ['arson','kidnapping','robbery','bombing','attack']
	self.weapons  = ["bomb", "rocket","nine powerful bombs", "vehicle", "powerful bomb", "explosive devices", "explosives loaded in a small truck", "four powerful rockets", "gun", "homemade bomb","m-79","m-16","bombs","GRENADES","DYNAMITE","MACHINE-GUN","car bomb", "machineguns in tripods", "ak-47s", "car bomb", "rocket", "machineguns in tripods", "ak-47s",  "terrorist bombs", "rifle","machine gun", "sniper", "sniper rifle", "pistol","AK-47", "M16", "AR-15", "MG42", "cannon","land mine", "mine", "artillery", "anthrax", "ricin", "tear gas", "nerve gas", "adamsite", "G3", "RPG-7", "UZI","longbow"]
        self.synonyms_for_keywords = {}
	self.synonyms_for_weapons = {}
        self.perp_indv = []
        self.perp_org = []
	self.targets = []
	self.victims = []
	self.nlp = spacy.load('en')
	self.f = open(filename+".template","w+")
	self.setup_key_words()
	self.setup_weapons()
        
	doc = self.nlp(u'')
	for possible_noun in doc:
		if possible_noun.pos_ == 'NOUN' and self.is_event(possible_noun.text):
    	 	        for possible_subject in possible_noun.children:
			    print(possible_subject.dep_)
		            if possible_subject.dep_ == 'nsubjpass':
                		print(possible_subject.text)
			    if possible_subject.dep_ == 'prep':
				 for possible_victim in possible_subject.children:
				 	print("Victim", possible_victim.text, possible_victim.pos_)				

				
							
	#for np in doc.noun_chunks:
	#	temp = np
	#	while (hasattr(temp,'root') and hasattr(temp.root,'head') and  temp.root.head.pos != VERB):	 		  
	#		print(temp.text, temp.root.text, temp.root.dep_, temp.root.head.text)
	#		print(temp.root.children)
	#		for possible_subject in temp.root.children:
	#			print("teja")
        #                  	print(possible_subject.text, possible_subject.dep_)
	#		temp = temp.root.head 
	#	if hasattr(temp,'root') and hasattr(temp.root,'head') and  temp.root.head.pos == VERB:
	#		print(temp.text, temp.root.text, temp.root.dep_, temp.root.head.text)
	   
 	self.event_extraction()
        self.f.close()
	print("the output is written to file "+filename+".template")
if __name__ == "__main__":
      e = EventExtraction(sys.argv[1])        
        
        
          
        
        
