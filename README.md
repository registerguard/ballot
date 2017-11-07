# ballot


### Online and print election results from Lane County  

![ballot](https://cloud.githubusercontent.com/assets/96007/15377445/8f7dc02c-1d10-11e6-8756-68438b1acf2a.png)

![screenshot 2016-05-18 14 50 01](https://cloud.githubusercontent.com/assets/96007/15378391/e74786ba-1d17-11e6-8828-80c8a730f442.png)

### Update: March 15, 2017

#### Pre/set up
1. Log in to server, use `$ python manage.py dumpdata ballot --format=json --indent=2 ... ` to export previous election as fixture (not there's a formal archive plan, it's just that straight-up deleting data gives me the willies ... ), then delete previous election data using web admin.
1. When running stuff locally, setup an SSH tunnel to production database
1. For Selenium, you may need to update chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads) to match desktop Chrome (which has probably been auto-updated a few times since you last used chromedriver). And the XPath description may have changed/need updating.

#### Once:
1. `ballot_upload_csv` (local)
1. (Looks like it's a good idea to update `LANE_CONTEST_IDS` in `ballot_settings.py` prior to running `ballot_setup` ... ) Quick & dirty hack; import .csv into Google Sheet, copy ID column into another tab and run `=UNIQUE(A:A)` on it from Column B. Copy & paste that column into BBEdit for grep cleanup (add indent & trailing comma). _Only copy the_ `LANE_CONTEST_IDS` _variable_ to the `ballot_settings.py` file on the server. The `local` and `remote` versions have different CSV_DIRECTORY locations!
1. `ballot_setup` (remote; a one-time-per-election thing)  

#### To update:
1. `python manage.py ballot_upload_csv` (local; browser-fake JavaScript click to download .csv, upload file to server)
2. `python manage.py ballot_process_csv` (remote; insert .csv data in server db)
3. `python manage.py ballot_upload_json` (local; make JSON from URL requests, upload to AWS S3 bucket)

--------
#### Old/pre-Nov. 1, 2016, setup:

Current hacky set-up:  

1. Make copies of:  
 * Previous year's Lane County set-up (file name format: `save_election_lane_setup_[YYYYMMDD].py`)
 * Lane County results update script (file name format: `election_lane_get_data_[YYYYMMDD].py`)
 * Oregon SOS results update script. (file name format: `election_oregon_sos_get_data_primary_[YYYYMMDD].py`) **Note**: There is no Oregon SOS set-up script as all the relevant races are driven by what's in the Lane County Elections races list.
1. Check around Lane County Elections web site for location of current Lane County ASCII Layout page, using last election's URL in set-up/update scripts as a starting place.
1. Run Lane set-up script.
1. Edit `contest_wrapper`s, `is_race`, `web_front`, `use_in_paper`, candidate names, race names.
1. Add out-of-county races.

On Election Night repeat this cycle:  

1. Run Lane County update script.
1. Run Oregon Secretary of State update script.
1. Clear Django cache.
1. Clear DTI Scraper cache.

###### Notes:

• Currently scripts run on `projects.registerguard.com` from the  `/rgcalendar/oper/scripts` directory.
• The principal and significant difference between primaries and general/special elections is that primaries have two (or three) versions of each contest: Democratic, Republican and/or Independent.
