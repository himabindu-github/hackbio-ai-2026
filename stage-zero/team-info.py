

# Creating a dictionary structure to store our details

all_bio_combined = {
    "team_member1": {
    "name":"Laura Mazzucchi",
     "affiliation":"a freelance researcher",
     "loved_gene":"rbcL, also known as RUBISCO",
     "organism":"all photosynthetic organisms",
    },


    "team_member2": {
    "name":"Himabindu Kumdam",
    "affiliation":"an independent learner",
    "loved_gene":"pdcd1",
    "organism":"humans"

    },

    "team_member3": {
        "name": "Devina Sharma",
        "affiliation": "an independent learner",
        "loved_gene": "TP53",
        "organism": "humans"

    },

    "team_member4": {
        "name": "Adeola Ayotope Oyesiji",
        "affiliation": "an independent learner",
        "loved_gene": "SOD1",
        "organism": "humans"

    },
}

#Using a for loop to iterate over each member

print("Hi there, we are team glutamine :), and we are part of the AI Genomic HackBio internship.\nRead below to learn more about us.")
for key in all_bio_combined:
    member = all_bio_combined[key]
    print(f"{member["name"]} works as {member["affiliation"]}. The gene of interest is {member["loved_gene"]}, "
          f"found in {member["organism"]}.")
