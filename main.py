
from geopy.geocoders.arcgis import ArcGIS
import pandas
import folium

#import geopy

from geopy.geocoders import Nominatim
from pandas.core.indexes.base import Index

nom = Nominatim(user_agent="my_request")
arcg = ArcGIS()

#map = folium.Map(location=[28.3682730180995, -80],tiles="Stamen Terrain",zoom_start=8)
map = folium.Map(location=[28.3682730180995, -81.56064998431161],zoom_start=8)

def geoloc(name):

    geoadr=""
    geolocation=""
    Home_Phone=""
    Mobile_Phone=""

    familydata = pandas.read_csv("Google_Contacts.csv")
    familydata = familydata.set_index("Full Name")
    familylist = familydata.loc[name,"Email":"Mobile Number"]
    n=list(familylist)
    #print(n[5]+n[7]+n[8]+str(n[9]))
    #loc = 'Taj Mahal, Agra, Uttar Pradesh 282001'
    try:
        loc = n[5]+","+n[7]+","+n[8]+" "+str(n[9])
    except:
        n=None
        geoadr="None"
        geolocation="None"
        Home_Phone="None"
        Mobile_Phone="None"
        Email="None"
    
    if n!=None:
        address = arcg.geocode(loc)
        loc2=list(address)
    if geoadr=="":
        geoadr=loc2[0]
        geolocation=loc2[1]
        Home_Phone=n[10]
        Mobile_Phone=n[11]
        Email = n[0]

    return geoadr,geolocation,Home_Phone,Mobile_Phone,Email

familydata = pandas.read_csv("Google_Contacts.csv")
familylist = familydata["Full Name"]
familylist = list(familylist)
fg = folium.FeatureGroup(name="family")
l=[]
for family in familylist:
    n=geoloc(family)
    if n[0]!="None":
        d={}
         #print(family+" "+str(n[0]+" "+str(n[1])))
        longitude = float(n[1][0])
        latitude = float(n[1][1])
        homephone = str(n[2])
        mobilephone = str(n[3])
        email = str(n[4])
        d["Full Name"] = family
        d["email"] = email
        d["Address"]= str(n[0])
        d["longitude"] = longitude
        d["latitude"]= latitude
        d["home phone"]= homephone
        d["mobile phone"]=mobilephone
        l.append(d)
        popupstr = "<b>"+d["Full Name"]+"</b><p>"+str(d["Address"])+"<p>Home phone:"+homephone+"</p><p>Mobile phone:"+mobilephone+"</p>"
        print(d["Full Name"]+" "+d["Address"]+" "+str(d["longitude"])+" "+str(d["latitude"]))
        fg.add_child(folium.Marker(location=[longitude,latitude], popup=popupstr, icon=folium.Icon(color='green')))


#print(l)
df = pandas.DataFrame(l)
map.add_child(fg)
map.save("index.html")
df.to_csv("Google_Contacts_Modified.csv",encoding='latin')