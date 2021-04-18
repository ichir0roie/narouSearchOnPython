import csv

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def createLatestMD():
    with open("../SaveData/latest.csv", "r", encoding="utf-8")as f:
        reader=csv.reader(f)
        data=[row for row in reader]

    with open("../SaveData/latest.md", "w", encoding="utf-8")as f:
        f.write("# latest.csv整理\n\n")

    for row in data[1:]:
        text=""

        text+="## "
        # text+=row[0]

        firstPage="https://ncode.syosetu.com/{0}/1/".format(row[1])

        text+="[{0}]({1})".format(row[0],firstPage)
        text+="\n\n"

        text+="+ ncode\n"
        text+="\t+ "+row[1]+"\n"

        text+="+ userid : "
        text+=str(row[2])+" | "
        text+="writer : "
        text+=row[3]+"\n"

        text+="+ length : {0}\n\n".format(str(row[5]))

        text+="### story\n\n"

        text+=row[4].replace("myTextEscapeEnter","  \n")

        text+="\n"

        with open("../SaveData/latest.md", "a", encoding="utf-8")as f:
            f.write(text)

def toHtmlForLatestMD():
    print("toHtml")
    import markdown
    with open("../SaveData/latest.md", "r", encoding="utf-8")as f:
        text=f.read()
    MD=markdown.Markdown()
    html=MD.convert(text)
    with open("../Settings/base.html", "r", encoding="utf-8")as f:
        baseHtml=f.read()

    newTabLabel='target="_blank" rel="noopener noreferrer"'
    html=html.replace('<a href="','<a {0} href="'.format(newTabLabel))

    with open("../SaveData/latest.html", "w", encoding="utf-8")as f:
        f.write(baseHtml)
        f.write(html)

def openHtmlForLatestHtml():
    print("toChrome")
    import subprocess
    chromePath='chrome'
    option=' --profile-directory="Profile 4"'
    import pathlib
    latestHtmlPath=str(pathlib.Path("../SaveData/latest.html").resolve())
    cmd=chromePath+" "+option+" "+latestHtmlPath
    subprocess.run(cmd)

def createAndOperHtml():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    createLatestMD()
    toHtmlForLatestMD()
    openHtmlForLatestHtml()

if __name__ == '__main__':
    createAndOperHtml()