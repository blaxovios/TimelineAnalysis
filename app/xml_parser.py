# Input xml file "dblp-2021-02-01.xml" where we fetch data.
input_file = r'C:\Users\tsepe\PycharmProjects\TimelineAnalysis\files\dblp-2021-02-01.xml'

# Output txt file "results.txt" where we save publications per year.
output_file = r'/files/results.txt'

def read_by_line():
    with open(input_file, 'r') as f:
        text = f.read()
        words = ["3d", "2d", "animation", "synthesize", "image", "gpu", "geometry", "rendering", "visualization", "art"
                 , "games", "effects", "imaging", "render", "photorealistic", "visual", "textures", "geometry"
                 , "polygonal", "fluid", "illumination", "shading", "surface", "relighting"]
        text = text.split("\n")
        count = dict()
        total = 0
        for itemIndex in range(len(text)):
            if text[itemIndex][1:6] == "title":
                for word in words:
                    if word in text[itemIndex]:
                        print(total, " : ", text[itemIndex][7:-8])
                        if "year" in text[itemIndex + 1]:
                            print(text[itemIndex + 1][6:10])
                            if text[itemIndex + 1][6:10] not in count:
                                count[text[itemIndex + 1][6:10]] = 1
                            else:
                                count[text[itemIndex + 1][6:10]] += 1
                                total += 1
                        break
    f = open(output_file, "w")
    f.write("Year" + "\t" + "Publications\n")
    for i in sorted(count):
        f.write((str(i) + "\t" + str(count[i]) + "\n"))
    f.close()
    d = count.items()
    sorted_items = sorted(d)
    print(sorted_items)
    print("Total publications: ", total)
read_by_line()
