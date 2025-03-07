import sqlite3
import os

conn = sqlite3.connect("data.db")
curr = conn.cursor()

curr.execute("SELECT DISTINCT Students.class FROM Students")
school_klassen_naam = curr.fetchall()


 # Create a directory if it doesn't exist
folder_name = "klassen_lijsten"
if not os.path.exists(folder_name):
        os.makedirs(folder_name)

for school_klas_naam in school_klassen_naam:
    schoolklas = school_klas_naam[0]
    print(schoolklas)
    curr.execute("SELECT Students.first_name, Students.last_name FROM Students WHERE Students.class = ?", (schoolklas,))
    klas = curr.fetchall()

    file_path = os.path.join(folder_name, schoolklas + ".txt")
    fhand = open(file_path, "w")

    klas_lengte = len(klas)
    fhand.write(schoolklas + "\n")
    fhand.write("Aantal leerlingen: " + str(klas_lengte))
    fhand.write("\n")
    fhand.write("\n")
    for name in klas :
        first_name = name[0]
        last_name = name[1]
        fullname = first_name + " " + last_name
        print(fullname)
        fhand.write(fullname + "\n")
    fhand.close()

# Stoute kinderen vangen

curr.execute("""SELECT Students.first_name, Students.last_name, Students.class 
FROM Students 
JOIN Schedule ON Students.student_id = Schedule.student_id 
WHERE round1_activity IS NULL 
  AND round2_activity IS NULL 
  AND round3_activity IS NULL 
  AND round4_activity IS NULL;
  """)
naughty_students = curr.fetchall()



file_path_naughty = os.path.join(folder_name, "naughty_list" + ".txt")
fhand = open(file_path_naughty, "w")
fhand.write("Lijst van leerlingen die hebben ingeschreven, maar geen enkele workshop hebben ingevuld." + "\n")
fhand.write("Aantal stoute leerlingen: " + str(len(naughty_students)) + "\n")
fhand.write("\n")
fhand.write("\n")

for naughty in naughty_students:
    first_name_naughty = naughty[0]
    last_name_naughty= naughty[1]
    the_class_of_naughty = naughty[2]
    naughty_kid = first_name_naughty + " " + last_name_naughty + " " + the_class_of_naughty
    fullname_naughty = first_name_naughty + " " + last_name_naughty
    print(naughty_kid)

    story = f"""
    Er was eens een leerling genaamd {fullname_naughty}, een slim maar ongelooflijk luie leerling dat in klas {the_class_of_naughty} van
    de middelbare school zit. {fullname_naughty} had een reputatie opgebouwd als de meester van het ontwijken van verantwoordelijkheden.
    Terwijl klasgenoten zich druk maakten om hun activiteiten voor de vier rondes van het schoolproject te kiezen—denk 
    aan sportdagen, kunstworkshops, wetenschapsclubs en meer—zat {fullname_naughty} achterin de klas met een grijns op zijn/haar gezicht. 
    "Waarom zou ik meedoen?" dacht {fullname_naughty}. "Ik vul gewoon niets in, en niemand zal het merken in al die chaos."
    """

    fhand.write(story)
    fhand.write("\n")



fhand.close()
conn.close() 