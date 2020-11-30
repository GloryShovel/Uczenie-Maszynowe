import yaml, os, sys

def select_file(extension, display=True, prompt="Select file: "):
    '''Allows to select file from a list of files of a given extension'''
    input_filenames = []
    for filename in os.listdir("."):
        if filename.endswith("."+extension):
            input_filenames.append(filename)
    input_filenames.sort()
    
    if display:
        print("Input files list:")
        if len(input_filenames) > 8:
            # Display files in columns
            input_filenames_A = input_filenames[:len(input_filenames)//2]
            input_filenames_B = input_filenames[len(input_filenames)//2:]
            print()
            maxlen = len(max(input_filenames_A, key=len))
            nl = 1
            nr = len(input_filenames_A)+1
            for i,j in zip(input_filenames_A, input_filenames_B):
                print("%d. %s\t%d. %s" % (nl,i.ljust(maxlen, " "), nr, j))
                nl = nl+1
                nr = nr+1
            if len(input_filenames_B) > len(input_filenames_A):
                print("%d. %s" % (nr,input_filenames_B[-1:][0]))
        else:
            # One-column
            for i in range(len(input_filenames)):
                print ("{}. {}".format(i+1,input_filenames[i]))
        
        print("0. Exit")
    
    # Collect the filename
    idx = -1
    while idx not in range(len(input_filenames)+1):
        try:
            idx = int(input(prompt))
        except ValueError:
            idx = 0
    if idx == 0:
        print("Exiting...")
        sys.exit()
    filename = input_filenames[idx-1]

    return(filename)


filename = select_file("yaml")

file = open(filename,"r",encoding='utf8')
data = yaml.safe_load(file)


print("Hipoteza, prawdopodobieństwo a priori (1/100%):")
for h in data["Hypotheses"]:
    print("{}, {}".format(h["name"], h["prob"]))

print()
print("POJEDYNCZE FAKTY")

# Calculate probability of facts
Pr_f = []
for fact in data["Facts"]:
    sum = 0
    for index,h in enumerate(data["Hypotheses"]):
        sum = sum + h["prob"]*fact["prob"][index]
    Pr_f.append([fact["name"],round(sum,5)])

print("Fakt, prawdopodobieństwo (1/100%):")
for x in Pr_f:
    print(*x, sep=", ")

# Calculate probability of hypothesis under a single fact
Pr_h_f = []
for indexh,h in enumerate(data["Hypotheses"]):
    for indexf,fact in enumerate(data["Facts"]):
        pr = round(h["prob"]*fact["prob"][indexh] / Pr_f[indexf][1],5)
        Pr_h_f.append([h["name"],fact["name"],pr])

print()
print("Hipoteza, fakt, prawdopodobieństwo (1/100%):")
for x in Pr_h_f:
    print(*x, sep=', ')


print()
print("KILKA FAKTÓW JEDNOCZEŚNIE")
print("Fakty:")
for index,fact in enumerate(data["Facts"]):
    print(index,fact["name"])


# Read list of facts
ok = False
while not ok:    
    selected_facts_indexes = sorted(input("Podaj numery objawów, oddzielając je spacjami: ").split())   
    # Convert to int
    selected_facts_indexes = [int(i) for i in selected_facts_indexes]
    # Remove duplicates
    selected_facts_indexes = list(dict.fromkeys(selected_facts_indexes))
    # Check if provided numbers are allowed    
    ok = set(selected_facts_indexes).issubset(range(len(data["Facts"])))

selected_facts = [data["Facts"][int(i)]["name"] for i in selected_facts_indexes]

'''
Zadanie: 
a) uzupełnić program tak, aby uwzględniał dowolne zestawy faktów
wg. wzoru w żółtej obwódce w pliku PDF,
b) utworzyć nowy plik z definicjami faktów, który mógłby posłużyć do wnioskowania o chorobach: COVID 19 / grypa / przeziębienie / inna choroba.
'''

# Calculate probability of hypothesis under a set of facts
# using formula "in yellow"


# Calculate the denominator of the formula
# The line below should be replaced by the actual calculations
denominator = 0
for ih,h in enumerate(data["Hypotheses"]):
    value = 1
    for index,fact in enumerate(data["Facts"]):
        if fact["name"] in selected_facts:
            value *= fact["prob"][ih]
    denominator += h["prob"] * value

for ih,h in enumerate(data["Hypotheses"]):
    # Calculate the numerator of the formula
    # The line below should be replaced by the actual calculations
    value = 1
    for index,fact in enumerate(data["Facts"]):
        if fact["name"] in selected_facts:
            value *= fact["prob"][ih]
    numerator = h["prob"] * value
   
    # Calculate, round and print the final result
    pr = round(numerator / denominator, 5)
    print("Prawdopodobieństwo hipotezy {} przy uwzględnieniu faktów ({}) wynosi: {}%."\
    .format(h["name"], ', '.join(selected_facts), round(pr*100, 5)))


