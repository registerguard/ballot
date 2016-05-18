# ballot

![ballot](https://cloud.githubusercontent.com/assets/96007/15377445/8f7dc02c-1d10-11e6-8756-68438b1acf2a.png)

![screenshot 2016-05-18 14 50 01](https://cloud.githubusercontent.com/assets/96007/15378391/e74786ba-1d17-11e6-8828-80c8a730f442.png)

### Online and print election results from Lane County

1. Make copies of previous year's Lane County set-up & update scripts and Oregon SOS update script. (There is no Oregon SOS set-up script as all the relevant races are in the Lane County races list.)
1. Check around Lane County Elections web site for location of current Lane County ASCII Layout page, using last election's URL in set-up/update scripts as a starting place.
1. Run Lane set-up script.
1. Edit `contest_wrapper`s, `is_race`, `web_front`, `use_in_paper`, candidate names, race names.
1. Add out-of-county races.

On Election Night repeat this cycle:  

1. Run Lane County update script.
1. Run Oregon Secretary of State update script.
1. Clear Django cache.
1. Clear DTI Scraper cache.
