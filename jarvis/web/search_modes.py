from __future__ import annotations
from enum import Enum
class SearchMode(str,Enum): SEARCH="search"; NEWS="news"; RESEARCH="research"; PRICE="price"; COMPARE="compare"
class SearchPlanner:
    def query(self,mode,query): return {"mode":SearchMode(mode).value,"query":query,"external_data_untrusted":True}
