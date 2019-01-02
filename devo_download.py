from requests import get
from azure.storage.blob import BlockBlobService

blob_service = BlockBlobService(account_name='renewedhope', sas_token='?sv=2018-03-28&ss=b&srt=sco&sp=rl&se=2020-01-01T12:41:27Z&st=2019-01-02T04:41:27Z&spr=https,http&sig=b45U%2BQtWDLTM79OFukl1b%2Fb2el0OEUvsGP68Dapa9Ws%3D')

blobs = blob_service.list_blobs('devotionals')
file_name_list = []
for b in blobs:
    #file_name_list.append(b.name)
    meta_data = blob_service.get_blob_properties('devotionals', b.name)
    print(b.name)
    print(meta_data.properties) # Can't get any useful info out of this

url_base = 'https://renewedhope.blob.core.windows.net/devotionals/'
file_name_base = r'C:\Users\drewc\Music\\'


def download(url, file_name):
    with open(file_name, 'wb') as file:
        response = get(url)
        file.write(response.content)


# for name in file_name_list:
#     url = url_base + name
#     file_name = file_name_base + name
#     download(url, file_name)
