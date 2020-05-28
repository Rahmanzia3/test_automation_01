import requests

from tqdm import tqdm

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024) as bar:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        bar.update(CHUNK_SIZE)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def un_zip(source,destination):
  
# specifying the zip file name 
    file_name = source
  
    # opening the zip file in READ mode 
    with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir() 
  
    # extracting all the files 
    print('Extracting all the files now...') 

    # ######## ADD DESTINATION LOCATION HERE
    zip.extractall(destination) 
    print('Done!') 





if __name__ == "__main__":
    from zipfile import ZipFile 
    import sys
    parser = ArgumentParser()
    parser.add_argument("--drive_id", required=True,type = str, help="id from google drive link")
    parser.add_argument("--download_dir", default='/app/darknet/custom_data/alpha.zip', required=True,type = str,help="Where you want to store zip file")

    parser.add_argument("--unzip_dir", default='/app/darknet/task/',required=True,type = str, help="Unzip dir should be in task dir")
    
    opt = parser.parse_args()
    google_drive_id = opt.drive_id
    download_directory = opt.download_dir
    extract_dir = opt.un_zip
    download_file_from_google_drive(google_drive_id, download_directory)
    un_zip(download_directory,extract_dir)


'''

BASIC FORMAT (DIRECT FROM GOOGLE DRIVE)
    https://drive.google.com/drive/my-drive

GENERATE SHARABLE LINK (PUBLIC VERSION)
    https://drive.google.com/file/d/18wIIagfAdD5NFt4HNlXYIkh6d0CjSWz3/view

THEN CLICK ON DOWNLOAD VERSION
    
    https://drive.google.com/uc?id=18wIIagfAdD5NFt4HNlXYIkh6d0CjSWz3&export=download


USE ID FROM THIS LINK
    
    18wIIagfAdD5NFt4HNlXYIkh6d0CjSWz3


OLD METHOD
    https://www.wonderplugin.com/online-tools/google-drive-direct-link-generator/


REQUIRED FORMAT

https://drive.google.com/uc?id=18wIIagfAdD5NFt4HNlXYIkh6d0CjSWz3&export=download

'''
