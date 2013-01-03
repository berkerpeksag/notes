# Notes

* naive datetime (datetime with no timezone information)
* localized time (datetime with current timezone information)
* önemli olan bir diğer şey de DST çevirimleri. Bizdeki GMT+2 ve GMT+3
  çevirimleri gibi bir şey. (yaz saati)
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
* **The preferred way of dealing with times is to always work in UTC,
  converting to localtime only when generating output to be read by humans.**

  ```py
  utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
  ```
* offset: dakika. offset değeri -1 gün ile 1 gün arasında olabilir.
* offset = 0 ise UTC.
*
### Links

* http://en.wikipedia.org/wiki/Pacific_Time_Zone
* http://en.wikipedia.org/wiki/Eastern_Time_Zone
* http://en.wikipedia.org/wiki/Coordinated_Universal_Time
* http://en.wikipedia.org/wiki/Time_zone

### Readings

* http://www.bryceboe.com/2012/11/05/time-zones-in-python-and-datetime-representations/
* http://www.upack.com/moving-services/articles/moving-across-the-world-a-guide-to-time-zones/
