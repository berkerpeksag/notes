# Notes

* naive datetime (datetime with no timezone information)
* localized time (datetime with current timezone information)
* önemli olan bir diğer şey de DST çevirimleri. Bizdeki GMT+2 ve GMT+3
  çevirimleri gibi bir şey. (yaz saati)
* Daylight saving does not affect UTC. It's just a polity deciding to change
  its timezone (offset from UTC). For example, GMT is still used: it's the
  British national timezone in winter. In summer it becomes BST.
* pytz bir tarihi verilen timezone'a çevirmek için iki yol sunuyor:

  **localize()**
  ```py
  eastern = timezone('US/Eastern')
  loc_dt = eastern.localize(datetime(2002, 10, 27, 6, 0, 0))
  print(loc_dt.strftime(fmt))
  ```

  **datetime.astimezone()**
  ```py
  utc = timezone('UTC')
  eastern = timezone('US/Eastern')
  dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
  loc_dt = dt.asttimezone(eastern)
  print(loc_dt.strftime(fmt))
  ```
* Other timezones can be written as an offset from UTC. Australian Eastern
  Standard Time is UTC+1000. e.g. 10:00 UTC is 20:00 EST on the same day.
* **The preferred way of dealing with times is to always work in UTC,
  converting to localtime only when generating output to be read by humans.**

  ```py
  utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
  ```
* offset: dakika. offset değeri -1 gün ile 1 gün arasında olabilir.
* offset = 0 ise UTC.
* **UTC:** The time at zero degrees longitude (the Prime Meridian) is called
  Universal Coordinated Time (UTC).
* **GMT:** UTC used to be called Greenwich Mean Time (GMT) because the Prime
  Meridian was (arbitrarily) chosen to pass through the Royal Observatory in
  Greenwich.

## UNIX Time

* Measured as the number of seconds since epoch (the beginning of 1970 in
  UTC). UNIXx time is not affected by time zones or daylight saving.
* Every day is exactly 86,400 seconds long.
* It's UTC. It's easy to obtain. It doesn't have timezone offsets or daylight
  saving (or leap seconds).

## Leap Seconds

* By international convention, UTC (which is an arbitrary human invention) is
  kept within 0.9 seconds of physical reality (UT1, which is a measure of
  solar time) by introducing a "leap second" in the last minute of the UTC
  year, or in the last minute of June.
* Leap seconds don't have to be announced much more than six months before
  they happen. This is a problem if you need second-accurate planning beyond
  six months.

## Best Practices

* When displaying time, always include the timezone offset. A time format
  without an offset is useless.

### Links

* http://en.wikipedia.org/wiki/Pacific_Time_Zone
* http://en.wikipedia.org/wiki/Eastern_Time_Zone
* http://en.wikipedia.org/wiki/Coordinated_Universal_Time
* http://en.wikipedia.org/wiki/Time_zone
* http://www.bbc.co.uk/news/world-13334229

### Readings

* http://www.bryceboe.com/2012/11/05/time-zones-in-python-and-datetime-representations/
* http://www.upack.com/moving-services/articles/moving-across-the-world-a-guide-to-time-zones/
* http://naggum.no/lugm-time.html
* [x] http://lucumr.pocoo.org/2011/7/15/eppur-si-muove/

### References

* http://unix4lyfe.org/time/
