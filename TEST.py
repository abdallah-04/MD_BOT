from google.oauth2.service_account import Credentials
import gspread
import random


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)


sheet_id = "1UPxC2R-C3fjSBwemS2bCa9AmcO4N3MYfMb0CEtCfY2Y"
sheet = client.open_by_key(sheet_id).sheet1  # Open the first sheet


# Get the last non-empty row using column B (names)
last_row = len(sheet.col_values(2))  # Fetch only column B

name = sheet.acell(f"B{last_row}").value
phone = sheet.acell(f"D{last_row}").value

# Display message
print(f"يعطيك العافيه {name} انا من IEEE computer society وانت مسجل بفورم الانضمام لسا حاب تسجل معنا ؟")
print(f"the WhatsApp link: https://wa.me/962{phone}")

# Mention a random MD member to conect him 
md_member = ["abdallah", "batool"]
print("@" + random.choice(md_member))
