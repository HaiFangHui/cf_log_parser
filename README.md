# HaiFangHui Toolsuite for download/parse CloudFront log


cf_log_parser is an data analysis tool used in HaiFangHui.com, to
download and parse CDN(cloudfront) logs, and store them in analytics
database for further study and research.

This tool would track which log files have already been processed, and
ignore them. This makes this tool very interesting when you have a
cronjob running every one hour or two to update your analytics
database.


# Install and use

```
# Download and install
git clone git@github.com:HaiFangHui/cf_log_parser.git
cd cf_log_parser

# Prepare virtual environment and libraries
virtualenv env
source env/bin/activate
pip install -r requirements.txt

# Config
cp log_parser.sample.cfg log_parser.cfg  
vi log_parser.cfg

# Run!
python download.py   # download/parse/store log files
```


# Use

Sample usages:

```
Find hot links:

SQL: select count(*), creferrer from log_entries where creferrer not like '%haifanghui%' group by creferrer;
```


```
Figure out what's the average size and traffic sum

select (avg(bytesent) / 1024)::int, (sum(bytesent)/1024/1024)::int from log_entries;
```
 
 
```
Someone is downloading aggressively?

select cip, count(*) as count, (sum(bytesent)/1024/1024)::int as traffic from log_entries group by cip order by traffic desc limit 5;
```


# TODO

We did not parse log entries using proper data format.
