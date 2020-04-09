
### Scrapy yelp

This python scraper for yelp was written to extract review information from businesses.

The main scraper class is located here
```bash
scrapy_yelp/scrapy_yelp/spiders/yelp.py
```


To crawl something simple we can do this
```
scrapy crawl yelp -a find='pizza' -a near='chicago'
```
which will generate a `summary.csv` and `menu.csv`

- **summary.csv** will contain aggregate information about the restaurant including the weighted score from yelp, and how many total reviews

- **menu.csv** will contain each menu item provided from yelp with (title,description,price) tuple.



For production run we can run all restauarants in chicago using a special keyword that reduces to all zip codes for chicago-metro area.  The `-s` switch also saves our crawl so we can pause/resume it for later.
```

scrapy crawl yelp  -s JOBDIR=crawls/spider-1 -a find='Restaurants' -a near='ALL_CHICAGO'
```


##### Full Production mode with historical

```
scrapy crawl yelp  -s JOBDIR=crawls/spider-all-crawls -a find='Restaurants' -a near='ALL'
```


### Catpcha ignore


```bash
brew install tesseract
```
Follow guidelines
https://github.com/owen9825/captcha-middleware



###### Fix I
```
vi +101 ~/git/foodcasting/deps/captcha-middleware/captchaMiddleware/solver.py  # remove mask arg           
```
```python
  contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
###### Fix II

```
vi +130 ~/git/foodcasting/deps/captcha-middleware/captchaMiddleware/solver.py  
````
```python
import imageio
....
imageio.imwrite(char_result +'.jpg', pil_image)
#scipy.misc.imsave(char_result + ".jpg", pil_image)
```

```bash
python setup.py test
python setup.py install
```

This did not work too well, although it may in the future, but for now I created a `selenium` instance on boot, and `captcha` will redirect to there.



```
 $= under $10. $$=11-30. $$$=31-60. $$$$= over $61.
 ```





 ### Statistics on crawling

It took 1000 seconds to crawl ~6100 yelp restaurants for the chicago-metro area (by zip code)

 ```
 2019-12-12 01:59:12 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 9156496,
 'downloader/request_count': 6399,
 'downloader/request_method_count/GET': 6399,
 'downloader/response_bytes': 258246237,
 'downloader/response_count': 6399,
 'downloader/response_status_count/200': 4409,
 'downloader/response_status_count/301': 1891,
 'downloader/response_status_count/303': 98,
 'downloader/response_status_count/404': 1,
 'dupefilter/filtered': 2125,
 'elapsed_time_seconds': 1015.320452,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2019, 12, 12, 9, 59, 12, 941192),
 'httperror/response_ignored_count': 1,
 'httperror/response_ignored_status_count/404': 1,
 'item_scraped_count': 2516,
 'log_count/DEBUG': 8916,
 'log_count/ERROR': 2,
 'log_count/INFO': 27,
 'memusage/max': 180162560,
 'memusage/startup': 115982336,
 'request_depth_max': 98,
 'response_received_count': 4410,
 'scheduler/dequeued': 6399,
 'scheduler/dequeued/disk': 6399,
 'scheduler/enqueued': 6399,
 'scheduler/enqueued/disk': 6399,
 'spider_exceptions/KeyError': 2,
 'start_time': datetime.datetime(2019, 12, 12, 9, 42, 17, 620740)}
2019-12-12 01:59:12 [scrapy.core.engine] INFO: Spider closed (finished)

```
