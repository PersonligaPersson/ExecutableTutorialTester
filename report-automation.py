print("Running the report automation script")

import requests
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import sys

# Get the PR number from the github action
pr_num = sys.argv[1]; # 0 is the file name

# Then fetch the reviews for that PR
url = f"https://api.github.com/repos/PersonligaPersson/ExecutableTutorialTester/pulls/{pr_num}/reviews"
print(f"Requesting on the url: ${url}")
response = requests.get(url)
print(f"reviews res: {response.status_code}")
res = response.json()

contributors = []
contributor_string = ""
if reponse.status._code != 200 or len(res) == 0:
    # If there are no reviews we use a default value.
    contributor_string = "no one"
else:
    # Otherwise we filter out the unique names.
    for review in res:
        user = review['user']['login']
        if user not in contributors:
            contributors.append(user)

    # Then format the output string
    if len(contributors) == 1:
        contributor_string = contributors[0]
    else:
        for i in range(len(contributors)-1):
            contributor_string += f"{contributors[i]}, "
        contributor_string = contributor_string[:len(contributor_string)-2]
        contributor_string += f" and {contributors[len(contributors)-1]}"


# Start by fetching data from the repository
# Todo: Change this to the current repo we're working with
url = "https://api.github.com/repos/KTH/devops-course/stats/contributors"
response = requests.get(url)
print(f"commits res: {response.status_code}")
res = response.json()

# Sort the contributors on the amount of commits.
res.sort(key = lambda x: x["total"], reverse = True)

# Grab the top 5.
top_contributors = []
for i in range(5):
  top_contributors.append({
      "name": res[i]["author"]["login"],
      "commits": res[i]["total"]
      })

# Then set up a bar plot show the top contributors.
bars = []
height = []
for item in top_contributors:
  bars.append(item["name"])
  height.append(item["commits"])

x_pos = np.arange(len(bars))

# Create bars and choose color
plt.bar(x_pos, height, color = (0.5,0.1,0.5,0.6))

# Add title and axis names
plt.title('Top Contributors')
plt.xlabel('Contributors')
plt.ylabel('Total Commits')

# Create names on the x axis
plt.xticks(x_pos, bars)

# Show graph
#plt.show()

# Save the graph
plt.savefig('topContributors.png')

# Now creat the PDF
fileName = 'Development_Statistics.pdf'
documentTitle = 'Development Statistics'
title = 'Feature Project Statistics'
subTitle = 'Development Statistics of our Latest Feature'
textLines = [
    'Top contributors to our latest feature are:',
]
image = 'topContributors.png'

# creating a pdf object
pdf = canvas.Canvas(fileName)

# Register a font
pdfmetrics.registerFont(
    TTFont('arial', 'arial.ttf')
)

# setting the title of the document
pdf.setTitle(documentTitle)

# creating the title by setting it's font
# and putting it on the canvas
pdf.setFont("arial", 26)
pdf.drawCentredString(300, 770, title)

# creating the subtitle by setting it's font,
# colour and putting it on the canvas
pdf.setFont("arial", 16)
pdf.drawCentredString(290, 720, subTitle)

# Present the reviewers
pdf.drawCentredString(290, 670, f"This feature was reviewed by: {contributor_string}")

# drawing a line
pdf.line(30, 710, 550, 710)

# creating a multiline text using
# textline and for loop
text = pdf.beginText(40, 620)
text.setFont("arial", 11)
#text.setFillColor(colors.red)

for line in textLines:
    text.textLine(line)

pdf.drawText(text)

# drawing a image at the
# specified (x.y) position
#pdf.drawInlineImage(image, 130, 400)
pdf.drawImage(image,20,300, 480, 360)

# saving the pdf
pdf.save()
