# Page that has the vote result link
SITE_ADDR = 'http://results.oregonvotes.gov/ResultsExport.aspx'

# For use in /ballot/results/full/
FINAL = False # If it's final results, set to True
ELECTION_DISPLAY_STRING = u'Nov. 7, 2017, special election'

# Directory on local machine that Selenium webdriver downloads files
CSV_DIRECTORY = '/Users/your/directory/here/'

# Names of the .csv files, xpath of where to click, db id of region to default
# association of each contest.
CSV_FILE_NAMES = (
    # Commenting out Statewide and Legistlative for May 16, 2017, Special
    # Election, which is all local results.
    #
    # {
    #     'file': 'Statewide_Media_Export.csv',
    #     'xpath': '//*[@id="MainContent_Statewide"]',
    #     'region_id': 2,
    #     'check_if_needed': True,
    # },
    # {
    #     'file': 'Legislative_Media_Export.csv',
    #     'xpath': '//*[@id="MainContent_Legislative"]',
    #     'region_id': 2,
    #     'check_if_needed': True,
    # },
    {
        'file': 'Lane_County_Media_Export.csv',
        'xpath': '//*[@id="MainContent_rptCountyExport_LinkButton1_19"]',
        'region_id': 4,
        'check_if_needed': False,
    },
)

JSON_URLS = (
    'http://foo.com/ballot/json/',
    'http://foo.com/ballot/json/url/',
    'http://foo.com/ballot/json/nuther-url/',
    'http://foo.com/ballot/json/yet-another/',
)

# scp machine & directory to upload to
SCP_STRING = 'user@machine.com:/directory/to/your/ballot/management/commands'

LANE_CONTEST_IDS = (
    100001833,
    100001833,
    100001834,
    100001834,
    100001835,
    100001835,
    100001836,
    100001836,
    100001837,
    100001837,
    100001838,
    100001838,
    100001846,
    100001846,
    100001847,
    100001847,
    100001850,
    100001850,
    100001853,
    100001853,
)
