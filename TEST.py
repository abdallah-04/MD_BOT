#high level api
from enum import member
import gspread
from google.oauth2.service_account import Credentials
import random

scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
]
creds= Credentials.from_service_account_file("credentials.json",scopes=scopes)
client =gspread.authorize(creds)

sheet_id="1UPxC2R-C3fjSBwemS2bCa9AmcO4N3MYfMb0CEtCfY2Y"
sheet=client.open_by_key(sheet_id)
B_count=2
D_count=2

phone=sheet.sheet1.acell(f"D{D_count}").value
name=sheet.sheet1.acell(f"B{B_count}").value

print(f"يعطيك العافيه {name} انا من IEEE computer society وانت مسجل بفورم الانضمام لسا حاب تسجل معنا ؟")
print(f"the wahtsapp link https://wa.me/962{phone}")
md_member=["abdallah","batool"]
print("@"+random.choice(md_member))
B_count+=1
D_count+=1