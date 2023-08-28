from cryptography.fernet import Fernet

a = "3E4MnH6MRFotROczxxMLwHG-70qYkqelhT0Tj2M1xjk="


b = "gAAAAABkhowIxeRbvl6C-bcFDVC9-aUObOhpvqomMQGcy9QOlntMWyk3EUGk7DBT3_eybNBN1sqgq07IpItK0MfnC8ukAXQaGIolyEG_Oq-hvAWDaHqFpz4="

key = a
f = Fernet(key)
print(f.decrypt(b))

#ALQ{F3rnet_eh_facinho_03}