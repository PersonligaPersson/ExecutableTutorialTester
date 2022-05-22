print("Running the report automation script")

import requests # import request library. 
import numpy as np
import matplotlib.pyplot as plt

url = "https://api.github.com/repos/KTH/devops-course/stats/contributors"
response = requests.get(url)
print("res: ", response.status_code)
res = response.json()
print(res)

# Sort the contributors on the amount of commits.
res.sort(key = lambda x: x["total"], reverse = True)

# Grab the top 5.
top_contributors = []
for i in range(5):
  top_contributors.append({
      "name": res[i]["author"]["login"],
      "commits": res[i]["total"]      
      })

# Print the top contributors
print(top_contributors)

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
plt.show()