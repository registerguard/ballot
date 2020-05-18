# ballot


### Online and print election results from Lane County  

![ballot](https://cloud.githubusercontent.com/assets/96007/15377445/8f7dc02c-1d10-11e6-8756-68438b1acf2a.png)

![screenshot 2016-05-18 14 50 01](https://cloud.githubusercontent.com/assets/96007/15378391/e74786ba-1d17-11e6-8828-80c8a730f442.png)

### Update: May 19, 2020

#### Pre-election set up notes
1. Log in to server, export previous election as a fixture: `$ python manage.py dumpdata ballot --format=json --indent=2 > ballot/fixtures/YYYYMMDD.json`, (**ProTip:** The date of the previous election's likely still kicking around in your `ELECTION_DISPLAY_STRING` variable in your `ballot/management/commands/ballot_settings.py` file! But if not, you can also look it up on the Lane County Elections site.) then, using the web admin delete all previous election data except for `Regions`. **Note:** Running `ballot_setup` (see below) also deletes `Cand_yes_no`, `Contest` and `Contest_wrapper` leaves `Region` intact, _but you it needs to have the Election IDs loaded, which it probably doesn't at this point, so ... _.
1. When running stuff locally, setup an SSH tunnel to production database
1. For Selenium, you may need to update chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads) to match desktop Chrome (which has probably been auto-updated a few times since you last used chromedriver). On Mac OS X, a location to move the `chromedriver` to that seems to work is `/usr/local/bin`.
1. Also, the XPath description may have changed on the Oregon SOS site and it may need updating in your `ballot/management/commands/ballot_settings.py` file so the scraper script can find it.

#### One-time set up stuff:
1. Run `ballot_upload_csv` (local). This tests out the Selenium grab of the .csv file from the Oregon Secretary of State web site. If successful, it gets you the Election IDs of all the contests, which you need to update `ballot_settings.py` below.
1. Update the `ELECTION_DISPLAY_STRING` in `/management/commands/ballot_settings.py` with the Election Day date and the type of election (special, general, primary ... ). 
> **NOTE:** As `ballot_settings.py` isn't in version control, once you've got it updated, you will have to update this manually both on your local machine and the remote server. BUT DON'T COPY THE ENTIRE FILE!
1. Update the `FINAL` template variable in `/management/commands/ballot_settings.py` to False (since it's probably set to True from the previous election being called final by the county clerk). This variable sets the "Unofficial/Official final" bit at the front of the title strings.
1. Update `LANE_CONTEST_IDS` in ` .../ballot_settings.py` prior to running `ballot_setup`  
**Quicker:** Visual Studio Code does vertical select, so open .csv created by `ballot_upload_csv` above, then `Option` + `Command` + `Down Arrow` ... but this won't get you the uniques, so you'll still need to upload to Googlge Sheet to remove dupe IDs. 
**Quick & dirty hack;** import .csv into Google Sheet, copy ID column into another Sheet and run `=UNIQUE(A:A)` on it from Column B. Copy & paste that column into BBEdit for grep cleanup (add indent & trailing comma).  
> **NOTE:** _Only copy the_ `LANE_CONTEST_IDS` _variable_ to the `ballot/management/commands/ballot_settings.py` file on the server (as opposed to copying the entire `ballot_settings.py` file). The `local` and `remote` versions of `ballot_settings.py` have different CSV_DIRECTORY locations! Also, remember to update remote `ELECTION_DISPLAY_STRING` and anything else you had to update in the local version. Like any tweaks/updates made to `CSV_FILE_NAMES`.  
And you will need to reload your Python code for the template string settings to appear, i.e., `touch apache/django.wsgi`.
1. `ballot_setup` (run it remote with `LANE_CONTEST_IDS` edits that you made locally; a one-time-per-election thing)  

#### One-time clean up of Measures, Races:
1. Once you've done the above, all the Measures and Races are imported into the Django db and by default are assigned to Lane County. You'll need use the Django admin `Ballot > Contests` to properly group the Federal, State, City etc. measures & races. 
> **Pro Tip:** Depending on the view that's powering your request, the quickest way to separate Measures from Races is the `is_race` attribute, which is easily edited in a bulk fashion from the admin `Contest` index view.

#### The Election Night steps to update results data:
1. `python manage.py ballot_upload_csv` (**local**; Uses Selenium to browser-fake JavaScript click to download .csv, uploads .csv file to server)
2. `python manage.py ballot_process_csv` (**remote**; insert .csv data in server db)
3. `python manage.py ballot_upload_json` (**local**; make JSON from URL requests, upload to AWS S3 bucket)
---

#### Other pieces:

`ballot_settings.py`: _local_ and _remote_: Different environmental settings for directories.  
`ballot_setup`: _remote_: After updating with new `LANE_CONTEST_IDS`, run once. Deletes previous election data, sets up new election fields. If you're running it locally to test, it's looking for the `.csv` files to be in the same directory as the script file (so you may need to copy them over from your `Downloads` directory).  
`ballot_test_data_in`: both  
`ballot_test_data_reset`: both  
`ballot_clear_cache`: _probably only remote_ Main web results page has a cached URL ('/ballot/results/full/') as well as a name template fragment cache ('main_results_table'). This clears both.

---
#### Obsolete, old/pre-Nov. 1, 2016, setup:

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
