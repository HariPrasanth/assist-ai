import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# Function to create folder if it doesn't exist
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Function to download a single page
def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text  # Get the text content for ReadTheDocsLoader
        return page_content
    else:
        print(f"Failed to download {url}")
        return None


# Main function to download the website
def download_website(url):
    page_content = download_page(url)
    if page_content:
        print("Page content retrieved successfully.")
        return page_content
    else:
        print("No content to process.")
        return None


# Function to save HTML content to a file
def save_content_to_file(content, url, language, folder):
    parsed_url = urlparse(url)
    filename = os.path.join(folder,
                            f"{language + parsed_url.netloc}_{parsed_url.path.strip('/').replace('/', '_')}.html")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved content to {filename}")
    return filename


# Function to read HTML content from a file and convert it into a document
def convert_html_to_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Assuming ReadTheDocsLoader is a placeholder for actual document processing function
    # Here, we are using BeautifulSoup to parse the HTML content and extract text
    soup = BeautifulSoup(html_content, 'html.parser')
    document_text = soup.get_text()
    return document_text


# URL of the website to download
def generate_link():
    dates = [
        "rahu-nakshtra-15th-july-24",
        "kashi-somwar-15th-july-2024",
        "omkareshwar-15th-july-24",
        "omkareshwar-jyotirlinga--15th-july-2024",
        "mangalwar-ram-vishesh-21st-july-2024",
        "mangalik-dosh-16th-july-2024",
        "dev-ekadashi-1-17th-july-24",
        "dev-ekadashi-2-17th-july-24",
        "dev-ekadashi-3-17th-july-2024",
        "narayan-bali-17th-july-2024",
        "19,000-mool-mantra-jaap-17th-july-2024",
        "dev-ekadashi-4-17th-july-2024",
        "pradosh-18july",
        "batuk-bhairav-18july",
        "tantrapeeth-19th-july-2024",
        "shani-puja-20th-july-2024",
        "baglamukhi-tantra-20july",
        "divya-maahakali-20th-july-24",
        "purnima-21st-1-2024",
        "rahu-guru-21july",
        "satyanarayan-katha-21july",
        "kashi-vishesh-21th-july-24",
        "guru-purnima-21st-july-2024",
        "jyotirlinga-vishesh-22nd-july-2024",
        "savan-22nd-july-2024",
        "savan-2nd-22nd-july-2024",
        "savan-somwar-22nd-july-2024"
    ]
    base_url = "https://srimandir.com/epuja/"
    download_folder = 'sm-puja-docs-latest'
    create_folder(download_folder)
    lang = ["en"]
    result = []
    for date in dates:
        for lan in lang:
            url = base_url + date + "?lang=" + lan
            print(url)
            result.append(url)
            page_content = download_website(url)
            if page_content:
                file_path = save_content_to_file(page_content, url, lan, download_folder)
                document = convert_html_to_document(file_path)
                print("Document content:")
                print(document)


# URL of the website to download
def generate_link_home():
    dates = [
        ""
    ]
    base_url = "https://srimandir.com/"
    download_folder = 'sm-home-docs'
    create_folder(download_folder)
    lang = ["hi", "en"]
    result = []
    for date in dates:
        for lan in lang:
            url = base_url + date + "?lang=" + lan
            print(url)
            result.append(url)
            page_content = download_website(url)
            if page_content:
                file_path = save_content_to_file(page_content, url, lan, download_folder)
                document = convert_html_to_document(file_path)
                print("Document content:")
                print(document)


# URL of the website to download
def generate_link_panchang():
    dates = [
        "01-07-2024",
        "02-07-2024",
        "03-07-2024",
        "04-07-2024",
        "05-07-2024",
        "06-07-2024",
        "07-07-2024",
        "08-07-2024",
        "09-07-2024",
        "10-07-2024",
        "11-07-2024",
        "12-07-2024",
        "13-07-2024",
        "14-07-2024",
        "15-07-2024",
        "16-07-2024",
        "17-07-2024",
        "18-07-2024",
        "19-07-2024",
        "20-07-2024",
        "21-07-2024",
        "22-07-2024",
        "23-07-2024",
        "24-07-2024",
        "25-07-2024",
        "26-07-2024",
        "27-07-2024",
        "28-07-2024",
        "29-07-2024",
        "30-07-2024"
    ]
    base_url = "https://srimandir.com/panchang/varanasi-uttar-pradesh-india/"
    download_folder = 'sm-panchang-docs'
    create_folder(download_folder)
    lang = ["hi", "en"]
    result = []
    for date in dates:
        for lan in lang:
            url = base_url + date + "?lang=" + lan
            print(url)
            result.append(url)
            page_content = download_website(url)
            if page_content:
                file_path = save_content_to_file(page_content, url, lan, download_folder)
                document = convert_html_to_document(file_path)
                print("Document content:")
                print(document)


def generate_link_temples():
    temples = [
        "ram-mandir",
        "iskcon-prayagraj",
        "nagvasuki-temple",
        "kalyanidevi-temple",
        "alopidevi-temple",
        "lalitadevi-temple",
        "nageshwarnath-temple",
        "devkali-temple",
        "hanuman-gadhi",
        "kanak-bhawan",
        "tretake-thakur",
        "rajdwar-temple",
        "birla-temple",
        "panchmukhimahadev-temple",
        "jalpadevi-temple",
        "suryakund-temple",
        "sitarasoi-temple",
        "kashivishwanath-temple",
        "maaannapurna-temple",
        "sankatha-temple",
        "sankatmochan-temple",
        "durga-temple",
        "kalbhairav-temple",
        "mrityunjayamahadev-temple",
        "bharatmata-temple",
        "gorakhnath-temple",
        "vishnu-temple",
        "geeta-vatika",
        "vishwanath-templebhu",
        "surajkund-dham",
        "tulsimanas-temple",
        "prachinhanuman-temple",
        "nandmahal-gokul",
        "mahaparinirvana-temple",
        "tarkulahadevi-temple",
        "budiyamai-temple",
        "dauji-temple",
        "mahavidyadevi-temple",
        "chamundadevi-temple",
        "keshavdev-temple",
        "kalimata-temple",
        "durga-temple1",
        "krishnajanmsthan-temple",
        "panchmukhihanuman-temple",
        "birla-temple1",
        "dwarkadhish-temple",
        "shrikalabhairav-temple",
        "chintamanganesh-temple",
        "harsiddhimata-temple",
        "ram-ghat",
        "dwarkadhishgopal-temple",
        "mahakaleshwar-ujjain",
        "ramjanardan-temple",
        "mangalnath-temple",
        "chousathyogini-temple",
        "ramjanaki-temple",
        "garhkalika-temple",
        "navagraha-temple",
        "iskconujjain-temple",
        "nidhivan-mandir",
        "shriradhavallabh-mandir",
        "shrijugalkishore-mandir",
        "prem-mandir",
        "isckon-templevrindavan",
        "bankebihari-temple",
        "radharaman-temple",
        "sriranganath-temple",
        "shahji-temple",
        "priyakantzoo-temple",
        "gopinath-temple",
        "madanmohan-temple",
        "jaipur-templevrindavan",
        "pagalbaba-temple",
        "vrindavanchandrodaya-temple",
        "radhashyamsundar-temple",
        "radhadamodar-temple",
        "katyayani-peeth",
        "gopeshwarmahadev-temple",
        "vrinda-kund",
        "anapurna-temple",
        "khajranaganesh-temple",
        "shrigopal-temple",
        "kanch-temple",
        "mahalaxmi-temple",
        "dutt-temple",
        "bijasanmata-temple",
        "badaganpatti-temple",
        "ranjithanuman-temple",
        "harsiddhimata-temple2",
        "bhooteshwer-temple",
        "chowbeesavtar-temple",
        "takshkeshwernath-temple",
        "sankatmochan-temple2",
        "navgrahshani-temple",
        "padilamahadev-temple",
        "patalpuri-temple",
        "vaishnodaam-temple",
        "govinddeviji-temple",
        "kalbhairav-indore",
        "shrivenimadhav-temple",
        "mankameshwer-temple",
        "shankarvimanamandapam-temple",
        "someshwermahadev-temple",
        "naxminarayan-temple",
        "gufa-temple",
        "bhojeshwer-temple",
        "manuabhantekri-temple",
        "gayatri-temple",
        "iskcon-templebhopal",
        "khatlapura-temple",
        "kankalimata-temple",
        "shrimadhyaswamimalayi-temple",
        "bharatmata-templeindore",
        "iskcon-radhagovind",
        "sheetla-matatemple",
        "geeta-bhawantemple",
        "mayadevi-templeharidwar",
        "harkipauri-temple",
        "neeleshwermahadev-temple",
        "bilvakeshwermahadev-temple",
        "iskcontemple-haridwar",
        "bharatmata-templeharidwar",
        "vaishnodevi-templeharidwar",
        "sureshwaridevi-templeharidwar",
        "dakshinkaali-temple",
        "avdhoothanuman-temple",
        "bhimgoudakund-temple",
        "dakshmahadev-temple",
        "chandidevi-templeharidwar",
        "pawandhaam-temple",
        "laxminarayan-temple",
        "ganga-ghat",
        "neelkanthmahadev-temple",
        "shribharat-temple",
        "kunjapuri-temple",
        "trimbakeshwar-temple",
        "raghunath-temple",
        "virbhadra-temple",
        "shatrughna-temple",
        "geeta-bhawan",
        "hanuman-temple",
        "triveni-ghat",
        "bhootnath-temple",
        "laxman-temple",
        "srivenkateswarawari-temple",
        "shreetapkeshwer-temple",
        "daatkalitemple-dehradun",
        "iskcontemple-dehradun",
        "shreekalikatemple-dehradun",
        "prakashehwertemple-dehradun",
        "laxminarayantemple-dehradun",
        "badahanumantemple-dehradun",
        "santaladevitemple-dehradun",
        "maabalasundaritemple-dehradun",
        "siddheshwertemple-dehradun",
        "manimayitemple-dehradun",
        "jageshwertemple-manaskhand",
        "goludevtatemple-manaskhand",
        "katarmalsuryadevtemple-manaskhand",
        "kasardevitemple-manaskhand",
        "nandadevitemple-manaskhand",
        "patalbhuwneshwergufa-manaskhand",
        "nainadevitemple-manaskhand",
        "baleshwertemple-manaskhand",
        "baijnathtemple-manaskhand",
        "varahidevitemple-manaskhand",
        "patalrudreshwergufa-manaskhand",
        "purngiritemple-manaskhand",
        "chandrabadnishaktipeeth-tehri",
        "surkandadevishaktipeeth-tehri",
        "haatkalikatemple-manaskhand",
        "bagnathtemple-manaskhand",
        "kaichidhamtemple-manaskhand",
        "chaitibalasundaritemple-manaskhand",
        "mayadevi-sidhpeethharidwar",
        "nainadevi-temple",
        "chandrabadni-shaktipeeth",
        "kunjapuri-mandir",
        "chaitibalasundari-temple",
        "purngiri-temple",
        "chandidevi-temple",
        "sureshwaridevi-temple",
        "anasuiyamata-temple",
        "mansadevi-haridwar",
        "mansadevi-shidhpeeth"
    ]
    base_url = "https://srimandir.com/temples/"
    download_folder = 'sm-temple-docs'
    create_folder(download_folder)
    lang = ["hi", "en"]
    result = []
    for temple in temples:
        for lan in lang:
            url = base_url + temple + "?lang=" + lan
            print(url)
            result.append(url)
            page_content = download_website(url)
            if page_content:
                file_path = save_content_to_file(page_content, url, lan, download_folder)
                document = convert_html_to_document(file_path)
                print("Document content:")
                print(document)


if __name__ == "__main__":
    generate_link()
    # generate_link_panchang()
    # generate_link_home()
    # generate_link_temples()
