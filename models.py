import gzip
import re
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, Text, func, desc
from config import config


db_spec = config.get('DATABASE', 'DB_SPEC')
engine = create_engine(db_spec)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True)
    logtime = Column(String(200))
    edge = Column(String(200))
    bytesent = Column(Integer)
    cip = Column(String(100))
    method = Column(String(20))
    host = Column(String(100))
    uri = Column(String(1024))
    status = Column(String(10))
    creferrer = Column(Text)
    useragent = Column(Text)
    cs_uri_query = Column(Text)
    cookie = Column(Text)
    x_edge_result_type = Column(Text)
    x_edge_request_id = Column(Text)
    x_host_header = Column(String(100))
    protocol = Column(String)
    cs_bytes = Column(Integer)
    time_taken = Column(String)

    def load_from(self, line):
        fields = line.split("\t")
        self.logtime = fields[0] + ' ' + fields[1]
        self.edge = fields[2]
        self.bytesent = fields[3]
        self.cip = fields[4]
        self.method = fields[5]
        self.host = fields[6]
        self.uri = fields[7]
        self.status = fields[8]
        self.creferrer = fields[9]
        self.useragent = fields[10]
        self.cs_uri_query = fields[11]
        self.cookie = fields[12]
        self.x_edge_result_type = fields[13]
        self.x_edge_result_id = fields[14]
        self.x_host_header = fields[15]
        self.protocol = fields[16]
        self.cs_bytes = fields[17]
        self.time_taken = fields[18]
        return self


class LogFile(Base):
    __tablename__ = 'log_files'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(100))


def parse_log_data(data):
    for line in data.splitlines():
        line.strip()
        if re.search('^#', line):
            pass
        else:
            log_entry = LogEntry()
            log_entry.load_from(line)
            session.add(log_entry)


