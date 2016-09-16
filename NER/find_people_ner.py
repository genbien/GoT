import collections

ner_file = 'GoT_ep01_chapter_scene_NER_from_tfidf_with_transcripts.txt'

def most_common(lst):
    data = collections.Counter(lst)
    return data.most_common(1)

with open(ner_file, 'r') as f:
	lines = f.read().splitlines()

i = 0
scenes = collections.OrderedDict()

while i < len(lines):
	if lines[i][0].isdigit():
		scenes[lines[i]] = []
		nb = lines[i]
		i += 1
		while lines[i][0].isalpha():
			tag, loc = lines[i].split(' ', 1)
			if tag == 'PERSON':
				scenes[nb].append(loc)
			i += 1
	i += 1


for scene in scenes:
	print scene, set(scenes[scene])











# 1 set(['Ser Waymar Royce', 'Mallisters', 'Wills', 'Ser Waymar', 'Gared', 'Will', "Ser Waymar 's", 'Mormont', 'Castle Black', 'Robert', 'Maester Aemon', 'Royce'])
# 2 set(['House Stark', 'Stark'])
# 3 set([])
# 4 set(['House Tully', 'Lord Eddard Stark', 'Robb Stark', 'Catelyn', 'Lady Catelyn', 'Bran Stark', 'Jon Snow'])
# 5 set(['Jeyne', 'Eddard Starks', 'Theon', 'Poor Jon', 'Stark', 'Beth Cassel', 'Rodrik', 'Tullys', 'Baratheon', 'Prince Tommen', 'Robb', 'Theon Greyjoy', 'Jeyne Poole', 'Myrcella', 'Joffrey', 'Rhoyne', 'Beth', "Ser Rodrik 's", 'Joff', 'Jon', 'Lew', 'Prince Joff', 'Mother', 'Winterfell', 'Arya', 'Bran', 'Ser Rodrik Cassel', 'Nymeria', 'Ser Rodrik', 'Sansa', 'Septa Mordane', 'Tommen', 'Lannister', 'Lady Catelyn', 'Rickon', 'Wed Tully'])
# 6 set(['Mance Rayder', 'Maester Luwin', 'Moat Cailin', 'Theon', 'Greyjoy', 'Father', 'Hullen', 'Quent', 'Rodrik', 'Starks', 'Wayn', 'Lannisters', 'Stiv', 'Lord Eddard', 'Robb', 'Joseth', 'Wyl', 'Osha', 'Theon Greyjoy', 'Hodor', 'Hal Mollen', "Benjen Stark 's", 'Lannister', 'Alyn', 'Hali', 'Rickon', 'Jon', 'Maester', 'Wallen', 'Hallis Mollen', 'Brandon Stark', 'Grey Wind', 'Stark', 'Mother', 'Wolves', 'Arya', 'Bran', 'Jory', 'Ser Rodrik Cassel', 'Benjen', 'Summer', 'Heward', 'Eddard', 'Dancer', 'Robb Stark', 'Luwin', 'Hack', 'Jory Cassel', 'Maester Pycelle', 'Jon Snow'])
# 7 set(['Eddard', 'Starks', 'Bran', 'Jon'])
# 8 set(['Mance Rayder', 'Theon', 'Robert', 'Father', 'Snow', 'Stark', 'Rodrik', 'Starks', 'Robb', 'Theon Greyjoy', 'House Stark', 'Warden', "Ser Rodrik 's", 'Greyjoy', 'Jon', 'Nan', 'Lord Eddard Stark', 'Hullen', 'Winterfell', 'Bran', 'Jory', 'Wall', 'Rickon', 'Eddard', 'Lord Stark', 'Jory Cassel', 'Jon Snow', 'Harwin'])
# 9 set(['Arryn', 'Robert', 'Cersei', 'Hand', 'Jaime', 'Robert Baratheon'])
# 10 set(['Catelyn'])
# 11 set(['Jon Arryn', 'Lysa', 'Eddard', 'Robin', 'Catelyn', 'Robert'])
# 12 set(['Jaime', 'Maester Luwin', 'Luwin', 'Catelyn', 'Cerseis'])
# 13 set(['Tommy', 'Robb', 'Jon', 'Theon'])
# 14 set(['Bran Stark', 'Catelyn'])
# 15 set(['Arya Stark', 'Stark'])
# 16 set(['Sansa', 'Eddard', 'Cersei', 'Stark', 'Jaime', 'Starks', 'Catelyn', 'Robert', 'Arya', 'Robb'])
# 17 set(['Jon Arryn', 'Theon', 'Robert Baratheon', 'Father', 'Snow', 'Stark', 'Brandon', 'Starks', 'Arryns', 'Lord Rickard Stark', 'Arryn', 'Sandor Clegane', 'Tywin Lannister', 'Wardens', 'Hand', 'Eddards', 'Catelyn Tully', 'Eddard Stark', 'Warden', 'Howland Reed', 'Lyanna', 'Ned', 'Jon', 'Lysa', 'Ser Jaime Lannister', 'Jaime', 'Seven Kingdoms', 'Dragonlords', 'Kingsguard', 'Winterfell', 'Rhaegar', 'Sansa', 'Eddard', "Balon Greyjoy 's", 'Cersei', 'Grace', 'Cersei Lannister', 'Lord Tywin', 'Lannister', 'Catelyn', 'Joff', 'Robert Arryn', 'Robert'])
# 18 set([])
# 19 set(['Benjen Stark', 'Lord Eddard', 'Robert', 'Stark', 'Brandon', 'Starks', 'Tyrion Lannister', 'Sandor Clegane', 'Joffrey', 'Tyrion', 'Jaime Lannister', 'Chayle', 'Jaime', 'Mother', 'Lady Stark', 'Winterfell', 'Myrcella', 'Tommen', "Sandor Clegane 's", 'Cersei', 'Clegane', 'Sandor', 'Ros', 'Ayrmidon', 'Targaryen'])
# 20 set(['Rhaegar Targaryen', 'Robert', 'Lyanna Stark', 'Eddard'])
# 21 set(['Dragonstone', 'Greyjoy', 'Khal Drogo', 'Father', 'Rhaesh Andahli', 'Dornishmen', 'Illyrio Mopatis', "Khal Drogo 's", 'Illyrio', 'Regal', 'Daenerys', 'Rhogoro', 'Westeros', 'Ser Willem', 'Targaryens', 'Magister', "Magister Illyrio 's", 'Daenerys Stormborn', 'Darry', 'Casterly Rock', 'Ser Jorah Mormont', 'Dany', 'Dothraki', 'Redwyne', 'Willem Darry', 'Kingslayer', 'Stark', 'Valyrian', 'Magister Illyrio', 'Viserys', 'Elia', 'Drogo', 'Tyrell', 'Rhaegar', 'Lys', 'Daenerys Targaryen', 'Myr', 'Valyria', 'Your Grace', 'Lannister', 'Ser Jorah', 'Khal Moro'])
# 22 set(['Vaes Dothrak', 'Jhiqui', 'Drogo', 'Haggo', 'Khaleesi', 'Dany', 'Daenerys Targaryen', 'Pentoshi', 'Mormont', 'Khal Drogo', 'Dothraki', 'Ser Jorah Mormont', 'Irri', 'Illyrio', 'Daenerys', 'Magister Illyrio', 'Ser Jorah', 'Viserys', 'Doreah'])
# 23 set(['Dragonstone', 'Greyjoy', 'Khal Drogo', 'Father', 'Rhaesh Andahli', 'Dornishmen', 'Illyrio Mopatis', "Khal Drogo 's", 'Illyrio', 'Regal', 'Daenerys', 'Rhogoro', 'Westeros', 'Ser Willem', 'Targaryens', 'Magister', "Magister Illyrio 's", 'Daenerys Stormborn', 'Darry', 'Casterly Rock', 'Ser Jorah Mormont', 'Dany', 'Dothraki', 'Redwyne', 'Willem Darry', 'Kingslayer', 'Stark', 'Valyrian', 'Magister Illyrio', 'Viserys', 'Elia', 'Drogo', 'Tyrell', 'Rhaegar', 'Lys', 'Myr', 'Valyria', 'Your Grace', 'Lannister', 'Ser Jorah', 'Khal Moro'])
# 24 set(['Stannis', 'Jeyne', 'Lord Eddard', "Jeyne Poole 's", 'Robert', 'Father', 'Queen Cersei', 'Jonquil', 'Prince Joffrey', 'Robb', 'Lord Hoster Tully', 'Arya', "Lord Petyr 's", 'Jeyne Poole', 'Joffrey', 'House Stark', 'Septa Mordane', 'Grace', 'Lord Petyr Baelish', 'Ser Mandon Moore', 'Varys', 'Ser Arys', 'Lord Baelish', 'Aemon', 'Sansas', 'Mother', 'Kingsguard', 'Ser Mandon', 'Lord Varys', 'Lord Petyr', 'Lady Shella', 'Sansa', 'Eddard', 'Cersei', 'Joff', 'Ser Boros', 'Cersei Lannister', 'Catelyn', 'Lady Catelyn', 'Vayon Poole', 'Littlefinger', 'Sweet Sansa'])
# 25 set(['Robert'])
# 26 set(['Jons', 'Benjen Stark', 'Summerwine', 'Theon', 'Robert', 'Stark', 'Cersei', 'Prince Joffrey', 'Baratheon', 'Lord', 'White', 'Robb', 'Tyrion Lannister', 'Ben Stark', 'Dorne', 'Maester Luwin', 'Warden', 'Tyrion', 'Robert Baratheon', 'Jon', 'Ghost', "Lord Tywin 's", 'Ben', 'Ser Jaime Lannister', 'Jaime', "Ned Stark 's", 'Hullen', 'Lady Stark', 'Winterfell', 'Arya', 'Laughter', 'Benjen', 'Sansa', 'Wall', 'Tommen', 'Queen Cersei', 'Daeren Targaryen', 'Uncle Benjen', 'Lannister', 'Jon Snow'])
# 27 set(['Benjen', 'Eddard', 'Robb'])
# 28 set(['Stannis', 'Jeyne', 'Lord Eddard', "Jeyne Poole 's", 'Robert', 'Father', 'Queen Cersei', 'Jonquil', 'Prince Joffrey', 'Robb', 'Lord Hoster Tully', 'Arya', "Lord Petyr 's", 'Jeyne Poole', 'Joffrey', 'House Stark', 'Septa Mordane', 'Grace', 'Lord Petyr Baelish', 'Ser Mandon Moore', 'Varys', 'Ser Arys', 'Lord Baelish', 'Aemon', 'Mother', 'Kingsguard', 'Ser Mandon', 'Lord Varys', 'Lord Petyr', 'Lady Shella', 'Sansa', 'Cersei', 'Joff', 'Ser Boros', 'Cersei Lannister', 'Catelyn', 'Lady Catelyn', 'Vayon Poole', 'Littlefinger', 'Sweet Sansa'])
# 29 set(['Robert', 'Jaime', 'Eddard Stark', 'Eddard', 'Jaime Lannister'])
# 30 set(['Ser Rodrik', 'Robert', 'Father', 'Hullen', 'Brandon', 'Tom', 'Robb', 'Jeyne Poole', 'Braavos', 'Hand', 'Porther', 'Eddard Stark', 'Alyn', 'Lyanna', 'Arya Stark', 'Rickon', 'Jon', 'Ned Stark', 'Nan', 'Mordane', 'Grieve', 'Mycah', 'Lord Eddard Stark', 'Fat Tom', 'Septon Chayle', 'Winterfell', 'Arya', 'Bran', 'Jory', 'Nymeria', 'Syrio Forel', 'Sansa', 'Septa Mordane', 'Myr', 'Needle', 'Catelyn', 'Vayon Poole', 'Harwin', 'Robbs', 'Mikken'])
# 31 set(['Benjen Stark', 'Luwin', "Lord Arryn 's", 'Ned', 'Stark', 'Brandon', 'Starks', 'Desmond', 'Dorne', 'Jon Arryns', "Ashara Dayne 's", 'Vale', 'Hand', 'Lady Arryn', 'Eddard Stark', 'King Robert', 'Arthur Dayne', 'Rickon', 'Robert', 'Jon', 'Edmure', 'Riverrun', 'Ben', "Ser Arthur 's", 'Lysa', 'Lannister', 'Winterfell', 'Arya', 'Bran', 'Jon Arryn', 'Benjen', 'Sansa', 'Eddard', 'Myr', 'Robb', 'Maester Luwin', 'Catelyn', 'Starfall', 'Jon Snow'])
# 32 set(['Vaes Dothrak', 'Jhiqui', 'Drogo', 'Khal Drogo', 'Khaleesi', 'Dany', 'Pentoshi', 'Mormont', 'Jorah', 'Dothraki', 'Ser Jorah Mormont', 'Haggo', 'Irri', 'Illyrio', 'Daenerys', 'Magister Illyrio', 'Ser Jorah', 'Viserys', 'Doreah'])
# 33 set(['Daenerys', 'Drogo'])
# 34 set(['Sandor Clegane', 'Sandor', 'Eddard', 'Robert', 'Bran'])
# 35 set(['Jaime', 'Cersei', 'Bran'])


