config = {
   'cors': {
       'allow_headers': [
           'Authorization', 'Origin', 'X-Requested-With',
           'Content-Type', 'Accept', 'X-Rate-Limit-Limit',
           'X-Rate-Limit-Remaining', 'X-Rate-Limit-Reset'
       ],
       'origins': '^((http?:\/\/)?(.*\.)?127\.0\.0\.1(?::\d{1,5})?).*',
   },
}
