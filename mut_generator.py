# -*- coding: utf-8 -*-
names = []
activities = []

with open("./log-reco.txt") as f:
	for line in f:
		line = line.split(';')
		if len(line) > 1:
			names.append(line[1])
			activities.append(line[2])

names = sorted(set(names))
activities = sorted(set(activities))

for i in range(0,len(activities)):
	activities[i] = activities[i]

with open ("./names.txt", 'w') as file_result:
	for name in names:
		file_result.write(name + '\n')

with open ("./activity.txt", 'w') as file_result:
	for activity in activities :
		file_result.write(activity)

mat_U = dict()
mat_U_bin = dict()

for name in names:
	mat_U[name] = dict()
	mat_U_bin[name] = dict()

for name in names:
	for activity in activities:
		mat_U[name][activity] = 0

with open("./log-reco.txt") as f:
	for line in f:
		line = line.split(';')
		if len(line) == 3:
			if line[2] in mat_U[line[1]]:
				mat_U[line[1]][line[2]] += 1
			else:
				mat_U[line[1]][line[2]] = 1


with open("./MUT.txt", "w") as matrice_result:
	for name in names:
		for activity in activities:
			matrice_result.write(str(mat_U[name][activity]))
			matrice_result.write(str(' '))
		matrice_result.write(str('\n'))

# Transformation binaire
with open("./MUT-Binaire.txt", "w") as matrice_result:
	for name in names:
		for activity in activities:
			mat_U_bin[name][activity] = 1 if (mat_U[name][activity] > 0) else 0
			matrice_result.write('1' if (mat_U[name][activity] > 0) else '0')
			matrice_result.write(str(' '))
		matrice_result.write(str('\n'))

# Matrices des distances entre thèmes
mat_D_theme = dict()
for activity in activities:
	mat_D_theme[activity] = dict()
	mat_D_theme[activity][activity] = 1

for index1 in range(0, len(activities)):
	for index2 in range(0, len(activities)):
		mat_D_theme[activities[index1]][activities[index2]] = 0

for activity in activities:
	mat_D_theme[activity][activity] = 1

for index1 in range(0, len(activities)-1):
	for index2 in range(index1+1, len(activities)):
		and_operator = 0
		or_operator = 0
		for name in names:
			if((mat_U[name][activities[index1]] > 0) and (mat_U[name][activities[index2]] > 0)):
				and_operator += 1
			elif((mat_U[name][activities[index1]]) != (mat_U[name][activities[index2]])):
				or_operator += 1
		mat_D_theme[activities[index1]][activities[index2]] = 1 - (float(and_operator) / float(or_operator))

with open("./MTT.txt", "w") as matrice_result:
	for index1 in range(0, len(activities)):
		for index2 in range(0, len(activities)):
			matrice_result.write(str(mat_D_theme[activities[index1]][activities[index2]]))
			matrice_result.write(str(' '))
		matrice_result.write(str('\n'))


print "Aperçu distances :"
print mat_D_theme

print "Fin !"
