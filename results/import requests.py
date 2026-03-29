import requests
from bs4 import BeautifulSoup
import csv
import base64
import time

base_url = "https://www.navodaya.gov.in/nvs/en/Admission-JNVST/Admission-Notifications/"
all_data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for page in range(1, 30):  # 29 pages
    try:
        url = base_url if page == 1 else f"{base_url}?page={page}"
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rows = soup.find_all('tr')
        
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 5:
                sno = cells[0].get_text(strip=True)
                title = cells[1].get_text(strip=True)
                date = cells[2].get_text(strip=True)
                file_type = cells[3].get_text(strip=True)
                
                link_elem = cells[4].find('a')
                if link_elem:
                    href = link_elem.get('href', '')
                    link_id = link_elem.get('id', '')
                    
                    # Direct URLs (external links or website links)
                    if href and href not in ['#', '/nvs/en/Admission-JNVST/Admission-Notifications/#']:
                        link = href
                    # Base64 encoded PDF IDs
                    elif link_id:
                        try:
                            decoded_id = base64.b64decode(link_id).decode('utf-8')
                            # Construct the download URL
                            link = f"https://www.navodaya.gov.in/nvs/export/sites/nvs/documents/{decoded_id}.pdf"
                        except:
                            link = f"BASE64_ID: {link_id}"
                    else:
                        link = "NO_LINK"
                else:
                    link = "NO_LINK_ELEMENT"
                
                all_data.append([sno, title, date, file_type, link])
        
        print(f"✓ Page {page} done ({len(all_data)} rows so far)")
        time.sleep(0.5)  # Be respectful to the server
        
    except Exception as e:
        print(f"✗ Page {page} error: {e}")
        continue

# Save to CSV
with open('navodaya_notifications_all.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['S.No.', 'Title', 'Publish Date', 'File Type/Size', 'Download Link'])
    writer.writerows(all_data)

print(f"\n✓ Extracted {len(all_data)} notifications to navodaya_notifications_all.csv")
