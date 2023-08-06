from simple_ddl_parser import DDLParser

ddl = """
    create table mytable (date timestamp_ntz, id number, content variant) cluster by (date, id);
    """
result = DDLParser(ddl).run(group_by_type=True, output_mode='bigquery')
import pprint

pprint.pprint(result)
