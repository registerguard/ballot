# ballot
 

### Online and print election results from Lane County  

![ballot](https://cloud.githubusercontent.com/assets/96007/15377445/8f7dc02c-1d10-11e6-8756-68438b1acf2a.png)

![screenshot 2016-05-18 14 50 01](https://cloud.githubusercontent.com/assets/96007/15378391/e74786ba-1d17-11e6-8828-80c8a730f442.png)

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
