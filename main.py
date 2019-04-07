from src.common.utils import *
from src.instagram.ApiCrawler import ApiCrawler
from src.instagram.Instagram import Instagram
from src.instagram.Analyser import database

config = loadConfiguration('config/config.yaml')
credentials = loadCredentials('config/credentials.yaml')
logger = getLogger(__name__)
'''logger.info("Initializing Instagram crawler, handle: "+credentials['instagram']['user'])
instagram = Instagram(credentials['instagram'], credentials['instagram']['user'])
logger.info("Instagram crawling completed for handle: "+credentials['instagram']['user'])'''
connect=database()
connect.db_connect()
connect.crawl_and_find(credentials)
connect.database_query()


