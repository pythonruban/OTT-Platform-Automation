import os
import configparser

config_dir = "./configuration/config.ini"

config = configparser.RawConfigParser()
config.read(config_dir)

class ReadConfig:
    
    @staticmethod 
    def getAdminPageURL():
        return config.get('url info', 'AdminPageURL')
    
    @staticmethod
    def getAdminId():
        return config.get('common info', 'AdminId')
    
    @staticmethod
    def getPassword():
        return config.get('common info', 'Password')
    @staticmethod
    def getUsernameId():
        return config.get('common info', 'UsernameId')
    
    @staticmethod
    def getPassId():
        return config.get('common info', 'PassId')
    
    @staticmethod
    def getAdvertiserPageURL():
        return config.get('url info', 'AdvertiserPageURL')
    
    @staticmethod
    def getHomePageURL():
        return config.get('url info', 'HomePageURL')
    
    @staticmethod
    def getTestingemail():
        return config.get('common info', 'Testingemail')
    
    @staticmethod
    def getTestpassword():
        return config.get('common info', 'Testpassword')
    
    @staticmethod
    def getAdverEmail():
        return config.get('common info', 'AdverEmail')
    
    @staticmethod
    def getAdverPassword():
        return config.get('common info', 'AdverPassword')
    
   