import requests
import json


def channel_by_region(region_code):
  channel_url = "https://iptv-org.github.io/iptv/channels.json"
  regions_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/scripts/data/regions.json"
  channel_data = requests.get(channel_url).json()
  regions_data = requests.get(regions_url).json()

  is_correct = False

  for continent in regions_data:
    if region_code.upper() in regions_data[continent]["codes"]:
      is_correct = True

  if is_correct:
    name_by_country = []
    for data in channel_data:
      try: 
        if data["countries"][0]["code"] == region_code:
          name_by_country.append(data['name'])
      except:
        pass
      
    return name_by_country
  else:
    return "no that code in here, please verify again"
  

def channel_by_categories(category):
  channel_url = "https://iptv-org.github.io/iptv/channels.json"
  categories_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/scripts/data/categories.json"
  channel_data = requests.get(channel_url).json()
  categories_data = requests.get(categories_url).json()

  is_correct = False

  for data in categories_data:
    if category in data["name"]:
      is_correct = True

  if is_correct:
    name_by_category = []
    for data in channel_data:
      try: 
        if data["category"] == category:
          name_by_category.append(data['name'])
      except:
        pass
      
    return name_by_category
  else:
    return "no that category in here, please verify again"


  
if __name__ == "__main__":
  print(channel_by_categories('Animation'))
  print(channel_by_region('kr'))
