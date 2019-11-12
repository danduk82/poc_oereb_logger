import os
import sys
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
 
class HttpLogs(Base):
    """
    The HttpLogs are the place where internal http access logs are stored. The
    can be used via scripts to display several usage statistics.

    Attributes:
        id (int): The identifier (primary key), only used for ensuring integrity of the contents
        service_type (str): the service type used. Possible values: [GetEGRID, GetExtractById,
            GetCapabilities, GetVersions]
        format (str): the requested format. Possible values: [xml, json, pdf]
        location_requested (str): the requested location
        http_status (int): the https response code
        flavour (str): one of [reduced, full, signed, embeddable], where
            applicable (this field can be NULL)
    """
########    __table_args__ = {'schema': 'test_logger'}
    __tablename__ = 'http_logs'
    log_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date = sa.Column(sa.DateTime, nullable=False)
    service_type = sa.Column(sa.String,
                             sa.CheckConstraint(
                                  """service_type in
                                  ('GetEGRID','GetExtractById','GetCapabilities','GetVersion')"""
                             ),
                             nullable=True)
    requested_format = sa.Column(sa.String,
                       sa.CheckConstraint("requested_format in ('xml','json','pdf')"),
                       nullable=True)
    location_requested = sa.Column(sa.String, nullable=True)
    http_status = sa.Column(sa.Integer, nullable=False)
    flavour = sa.Column(sa.String, nullable=True)
    def __init__(self, date, http_status, log_id=None, service_type=None,
                 requested_format=None, location_requested=None, flavour=None):
         self.date=date
         self.http_status=http_status
         self.log_id=log_id
         self.service_type=service_type
         self.requested_format=requested_format
         self.location_requested=location_requested
         self.flavour=flavour

