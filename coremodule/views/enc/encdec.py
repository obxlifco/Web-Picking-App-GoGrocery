from hashlib import sha256
import base64
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]

class AESCipher:

    def __init__( self, key ):
        self.key = bytes(key, 'utf-8')
        print("key="+str(self.key))
    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        # iv = "encryptionIntVec"
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        # iv = "encryptionIntVec"
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] )).decode('utf-8')

cipher = AESCipher('mysecretpassword')

data = {
    "status": 1,
    "data": [
        {
            "id": 4,
            "parent_id": 0,
            "display_order": 1,
            "name": "test hv ch",
            "description": "ehgf jdshjs dhgkjshg",
            "image": "",
            "thumb_image": "",
            "banner_image": "",
            "page_title": "test hv ch",
            "category_url": "http://192.168.0.125:8085/category/test-hv-ch-",
            "slug": "test-hv-ch",
            "CatId": 4,
            "ParentId": 0,
            "DisplayOrder": 1,
            "CatName": "test hv ch",
            "CatDescription": "ehgf jdshjs dhgkjshg",
            "CatImage": "",
            "CatThumbImage": "",
            "CatBannerImage": "",
            "PagTitle": "test hv ch",
            "CatSlug": "test-hv-ch"
        },
        {
            "id": 2,
            "parent_id": 0,
            "display_order": 2,
            "name": "Beverages",
            "description": "Beverages",
            "image": "",
            "thumb_image": "",
            "banner_image": "",
            "page_title": "Beverages",
            "category_url": "http://localhost:8087/category/beverages",
            "slug": "beverages",
            "CatId": 2,
            "ParentId": 0,
            "DisplayOrder": 2,
            "CatName": "Beverages",
            "CatDescription": "Beverages",
            "CatImage": "",
            "CatThumbImage": "",
            "CatBannerImage": "",
            "PagTitle": "Beverages",
            "CatSlug": "beverages",
            "child": [
                {
                    "id": 1,
                    "parent_id": 2,
                    "display_order": 1,
                    "name": "Edible Oil",
                    "description": "Oil",
                    "image": "",
                    "thumb_image": "",
                    "banner_image": "",
                    "page_title": "Edible Oil",
                    "category_url": "http://localhost:8087/category/edible-oil",
                    "slug": "edible-oil",
                    "CategorBanner": [
                        {
                            "id": 4,
                            "website_id": 1,
                            "banner_name": "Carpet",
                            "created": "2018-02-01T11:25:17Z",
                            "modified": "2018-02-01T11:25:17Z",
                            "isdeleted": "n",
                            "isblocked": "n",
                            "category_id": 1,
                            "banner_link_to": "category",
                            "applicable_for": "category",
                            "banner_type": "c",
                            "parent_id": 1,
                            "is_notification_enabled_val": "n",
                            "notification_msg": "n"
                        }
                    ],
                    "CatId": 1,
                    "ParentId": 2,
                    "DisplayOrder": 1,
                    "CatName": "Edible Oil",
                    "CatDescription": "Oil",
                    "CatImage": "",
                    "CatThumbImage": "",
                    "CatBannerImage": "",
                    "PagTitle": "Edible Oil",
                    "CatSlug": "edible-oil",
                    "child": [
                        {
                            "id": 5,
                            "parent_id": 1,
                            "display_order": 2,
                            "name": "test category 2",
                            "description": "xdshgzdsfhzdf zhfz",
                            "image": "HeaderImage_test-category-2.jpg",
                            "thumb_image": "",
                            "banner_image": "bannerImage_test-category-2.jpg",
                            "page_title": "test category 2",
                            "category_url": "http://localhost:8087/category/test-category-2",
                            "slug": "test-category-2",
                            "CatId": 5,
                            "ParentId": 1,
                            "DisplayOrder": 2,
                            "CatName": "test category 2",
                            "CatDescription": "xdshgzdsfhzdf zhfz",
                            "CatImage": "HeaderImage_test-category-2.jpg",
                            "CatThumbImage": "",
                            "CatBannerImage": "bannerImage_test-category-2.jpg",
                            "PagTitle": "test category 2",
                            "CatSlug": "test-category-2"
                        }
                    ]
                },
                {
                    "id": 3,
                    "parent_id": 2,
                    "display_order": 1,
                    "name": "test company name",
                    "description": "test description",
                    "image": "",
                    "thumb_image": "",
                    "banner_image": "",
                    "page_title": "test company name",
                    "category_url": "http://localhost:8087/category/test-company-name",
                    "slug": "test-company-name",
                    "CatId": 3,
                    "ParentId": 2,
                    "DisplayOrder": 1,
                    "CatName": "test company name",
                    "CatDescription": "test description",
                    "CatImage": "",
                    "CatThumbImage": "",
                    "CatBannerImage": "",
                    "PagTitle": "test company name",
                    "CatSlug": "test-company-name"
                }
            ]
        }
    ]
}
# datax = str(data)
# encrypted = cipher.encrypt(datax)
# decrypted = cipher.decrypt(encrypted)
# print("++++++++++++++ Encripted ++++++++++++++++++++++")
# print(encrypted)
# print("++++++++++++++ Decrypted ++++++++++++++++++++++")
# print(decrypted)

