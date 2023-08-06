from pyspark.sql.types import StructType
from pyspark.sql import functions as F
from simple_salesforce import Salesforce
import datetime
import json
import pandas as pd

class Sfdc:
    """
    Salesforce Connection
    """

    def __init__(
        self,
        sfdc_conn: any,
        spark_session: any = None,
        frame_type: str = "pandas",
        field_threshold: int = 400,
        filter_threshold: int = 100,
    ):

        if frame_type not in ["pandas", "spark"]:
            raise ValueError("Invalid data frame type")
        self.conn = sfdc_conn
        self.frame_type = frame_type
        self.spark = spark_session
        self.field_threshold = field_threshold
        self.filter_threshold = filter_threshold
        self.column_count: int = 0
        self.erd = {
            "Opportunity": {
                "Keys": ["Id", "LastModifiedDate"],
                "Child": {"Quote": "Id"},
            },
            "Quote": {
                "Keys": ["Id", "LastModifiedDate"],
                "Parent": {"Opportunity": "OpportunityId"},
                "Child": {"QuoteLineItem": "Id"},
            },
            "QuoteLineItem": {
                "Keys": ["Id", "LastModifiedDate"],
                "Parent": {"Quote": "QuoteId"},
            },
        }

    def __eval_limit(self, limit: int = None):
        filter = ""
        if limit:
            filter = f" LIMIT {limit}"
        return filter

    def __gen_id_filter(
        self, key_filter: str = None, id_list: any = None, multi_filter: bool = False
    ):
        filter = ""
        key = "Id"
        if key_filter:
            key = key_filter
        if id_list:
            if not isinstance(id_list, list):
                id_list = id_list.to_list()
            if multi_filter:
                filter = f""" AND {key} in ('{("','").join(id_list)}')"""
            else:
                filter = f""" WHERE {key} in ('{("','").join(id_list)}')"""
        return filter

    def __gen_date_filter(
        self,
        key_filter: str = None,
        start_dt: datetime = None,
        end_dt: datetime = None,
        multi_filter: bool = False,
    ):
        filter = ""
        key = "LastModifiedDate"
        if key_filter:
            key = key_filter
        if start_dt:
            start = start_dt.replace(tzinfo=datetime.timezone.utc).isoformat()
            end = end_dt.replace(tzinfo=datetime.timezone.utc).isoformat()
            if multi_filter:
                filter = f""" AND {key} >= {start} AND {key} <= {end})"""
            else:
                filter = f""" WHERE {key} >= {start} AND {key} <= {end}"""
        return filter

    def __gen_soql(
        self,
        fields: list,
        object: str,
        date_filter: str = "",
        id_filter: str = "",
        limit: str = "",
    ):
        query = (
            f"SELECT {(',').join(fields)} FROM {object}{date_filter}{id_filter}{limit}"
        )
        return query

    def __get_child_relationship(self, erd: dict, primary: str):
        parent_obj = None
        child_obj = None
        if "Parent" in erd[primary]:
            parent_obj = list(erd[primary]["Parent"].keys())[0]
        if "Child" in erd[primary]:
            child_obj = list(erd[primary]["Child"].keys())[0]
        return primary, parent_obj, child_obj

    def __get_object_fields(self, salesforce_object: str, query_keys: list):
        sf_obj = getattr(self.conn, salesforce_object)
        desc = sf_obj.describe()
        field_names = [
            field["name"] for field in desc["fields"] if field["name"] not in query_keys
        ]
        field_names.sort()
        return field_names

    def __fetch_data(
        self,
        salesforce_object: str,
        fields: list,
        key_filter: any = None,
        date_key_filter: any = None,
        id_filter: any = None,
        start_dt: datetime = None,
        end_dt: datetime = None,
        limit: int = None,
    ):
        date_mf = False
        id_mf = False
        if start_dt and id_mf:
            id_mf = True
        result = self.conn.query(
            self.__gen_soql(
                fields=fields,
                object=salesforce_object,
                date_filter=self.__gen_date_filter(
                    date_key_filter, start_dt, end_dt, date_mf
                ),
                id_filter=self.__gen_id_filter(key_filter, id_filter, id_mf),
                limit=self.__eval_limit(limit),
            )
        )
        return result

    def __read_dataframe(self, result: any, master_dataframe: any = None):
        if result["records"]:
            if self.frame_type == "pandas":
                dataframe = pd.json_normalize(result["records"])
                dataframe = dataframe.loc[
                    :, ~dataframe.columns.str.startswith("attributes.")
                ]
                if master_dataframe is not None:
                    if not master_dataframe.empty:
                        dataframe = pd.concat([master_dataframe, dataframe])
            if self.frame_type == "spark":
                # dataframe = self.spark.createDataFrame(result["records"])
                j = json.dumps(result["records"])
                dataframe = self.spark.read.json(sc.parallelize([j]))
                cols = dataframe.columns
                # print(len(cols), cols)
                cols_to_drop = [x for x in cols if x.startswith("attributes")]
                print(cols_to_drop)
                dataframe = dataframe.drop(*cols_to_drop)
                if master_dataframe:
                    if master_dataframe.count() != 0:
                        dataframe = master_dataframe.union(dataframe)
        else:
            if self.frame_type == "spark":
                if master_dataframe:
                    if master_dataframe.count() != 0:
                        dataframe = master_dataframe
                else:
                    dataframe = self.spark.createDataFrame([], StructType([]))
            if self.frame_type == "pandas":
                if master_dataframe:
                    if not master_dataframe.empty:
                        dataframe = master_dataframe
                else:
                    dataframe = pd.DataFrame()
        return dataframe

    def __bulk_fetch_data(
        self,
        salesforce_object: str,
        query_fields: list,
        key_filter: str = None,
        date_key_filter: str = None,
        id_filter: list = None,
        start_dt: datetime = None,
        end_dt: datetime = None,
        limit: int = None,
    ):
        result = self.__fetch_data(
            salesforce_object=salesforce_object,
            fields=query_fields,
            key_filter=key_filter,
            date_key_filter=date_key_filter,
            id_filter=id_filter,
            start_dt=start_dt,
            end_dt=end_dt,
            limit=limit,
        )
        dataframe = self.__read_dataframe(result)
        while not result["done"]:
            result = self.conn.query_more(result["nextRecordsUrl"], True)
            dataframe = self.__read_dataframe(result, dataframe)

        return dataframe

    def bulk_query(
        self,
        salesforce_object: str,
        query_keys: list = [],
        prefix: str = None,
        key_filter: str = None,
        id_filter: list = None,
        start_dt: datetime = None,
        end_dt: datetime = None,
        limit: int = None,
    ):
        """
        To be Developed: URI too long error - dynamic dividend parameter adjustment
        """
        fields = self.__get_object_fields(salesforce_object, query_keys)
        dividend = len(fields) + len(query_keys)
        if dividend > self.field_threshold:
            dividend = int(dividend / (dividend / self.field_threshold)) + 1
            bulk_dataframe = self.__bulk_fetch_data(
                salesforce_object=salesforce_object,
                query_fields=query_keys,
                key_filter=key_filter,
                id_filter=id_filter,
                start_dt=start_dt,
                end_dt=end_dt,
                limit=limit,
            )

        print(
            f"{salesforce_object} -- Total fields: {len(fields) + len(query_keys)}, Dividend: {dividend}"
        )
        self.column_count += len(fields) + len(query_keys)
        for i in range(0, len(fields), dividend):
            print(i, dividend + i)
            query_fields = query_keys + fields[i : i + dividend]
            dataframe = self.__bulk_fetch_data(
                salesforce_object=salesforce_object,
                query_fields=query_fields,
                key_filter=key_filter,
                id_filter=id_filter,
                start_dt=start_dt,
                end_dt=end_dt,
                limit=limit,
            )

            if dividend != len(fields) + len(query_keys):
                if self.frame_type == "pandas":
                    if not bulk_dataframe.empty:
                        bulk_dataframe = bulk_dataframe.merge(
                            dataframe,
                            left_on=query_keys,
                            right_on=query_keys,
                            how="left",
                        )

                if self.frame_type == "spark":
                    if bulk_dataframe.count() != 0:
                        bulk_dataframe = bulk_dataframe.join(
                            dataframe, on=query_keys, how="left"
                        )
            else:
                bulk_dataframe = dataframe

        if prefix:
            if self.frame_type == "pandas":
                bulk_dataframe = bulk_dataframe.add_prefix(f"{prefix}__")
            if self.frame_type == "spark":
                bulk_dataframe = bulk_dataframe.select(
                    [F.col(x).alias(f"{prefix}__" + x) for x in dataframe.columns]
                )

        return bulk_dataframe

    def change_event_query(
        self,
        sfdc_change_object: str,
        erd: dict = None,
        id_filter: list = None,
        limit: int = None,
    ):
        if not id_filter:
            raise ValueError("Missing Input Parameter: id_filter")

        if not erd:
            erd = self.erd
        # Query change object
        change_object_dataframe = self.bulk_query(
            salesforce_object=sfdc_change_object,
            query_keys=erd[sfdc_change_object]["Keys"],
            prefix=sfdc_change_object,
            id_filter=id_filter,
            limit=limit,
        )
        # Query parents
        primary, parent, child = self.__get_child_relationship(erd, sfdc_change_object)
        while parent:
            primary_val = f"{primary}__{erd[primary]['Parent'][parent]}"
            parent_val = f"{parent}__{erd[parent]['Child'][primary]}"
            filter_key = f"{erd[parent]['Child'][primary]}"
            records = list(change_object_dataframe[primary_val].dropna())
            merge_dataframe = self.bulk_query(
                salesforce_object=parent,
                query_keys=erd[parent]["Keys"],
                prefix=parent,
                key_filter=filter_key,
                id_filter=records,
                limit=limit,
            )
            if self.frame_type == "pandas":
                if merge_dataframe.empty:
                    break

                change_object_dataframe = merge_dataframe.merge(
                    change_object_dataframe,
                    right_on=primary_val,
                    left_on=parent_val,
                    how="left",
                )

            if self.frame_type == "spark":
                if merge_dataframe.count() == 0:
                    break

                change_object_dataframe = merge_dataframe.join(
                    change_object_dataframe, on=primary_val, how="left"
                )

            primary, parent, child = self.__get_child_relationship(erd, parent)

        # Query children
        primary, parent, child = self.__get_child_relationship(erd, sfdc_change_object)
        while child:
            primary_val = f"{primary}__{erd[primary]['Child'][child]}"
            child_val = f"{child}__{erd[child]['Parent'][primary]}"
            filter_key = f"{erd[child]['Parent'][primary]}"
            if self.frame_type == "pandas":
                records = list(change_object_dataframe[primary_val].dropna())
            if self.frame_type == "spark":
                records = (
                    (change_object_dataframe.select(primary_val).na.drop())
                    .rdd.flatMap(lambda x: x)
                    .collect()
                )
            merge_dataframe = self.bulk_query(
                child,
                query_keys=erd[child]["Keys"],
                prefix=child,
                key_filter=filter_key,
                id_filter=records,
                limit=limit,
            )
            if self.frame_type == "pandas":
                if merge_dataframe.empty:
                    break
                change_object_dataframe = change_object_dataframe.merge(
                    merge_dataframe, left_on=primary_val, right_on=child_val, how="left"
                )

            if self.frame_type == "spark":
                if merge_dataframe.count() == 0:
                    break

                change_object_dataframe = change_object_dataframe.join(
                    merge_dataframe,
                    change_object_dataframe.select(primary_val)
                    == merge_dataframe.select(child_val),
                    how="left",
                )

            primary, parent, child = self.__get_child_relationship(erd, child)

        return change_object_dataframe

    def query_erd(
        self,
        sfdc_parent_object: str,
        start_dt: datetime = None,
        end_dt: datetime = None,
        erd: dict = None,
        limit: int = None,
    ):

        if not erd:
            erd = self.erd
        child_obj = list(erd[sfdc_parent_object]["Child"].keys())[0]
        primary_val = f"{erd[sfdc_parent_object]['Child'][child_obj]}"
        object_dataframe = self.__bulk_fetch_data(
            salesforce_object=sfdc_parent_object,
            query_fields=erd[sfdc_parent_object]["Keys"],
            start_dt=start_dt,
            end_dt=end_dt,
            limit=limit,
        )

        dataframe = None
        if self.frame_type == "pandas":
            if not object_dataframe.empty:
                records = list(object_dataframe[primary_val])

                # Start test iter
                print("NUM OF RECORDS:", len(records))
                bulk_dataframe = pd.DataFrame()
                dividend = len(records)
                if dividend > self.filter_threshold:
                    dividend = int(dividend / (dividend / self.filter_threshold)) + 1

                iter_cnt = 0
                for i in range(0, len(records), dividend):
                    print(i, dividend + i)
                    iter_cnt += 1
                    query_records = records[i : i + dividend]
                    # End test iter
                    dataframe = self.change_event_query(
                        sfdc_change_object=sfdc_parent_object,
                        id_filter=query_records,  # records
                    )
                    dataframe = pd.concat([bulk_dataframe, dataframe])

                self.column_count = int(self.column_count / iter_cnt)

        if self.frame_type == "spark":
            if object_dataframe.count() != 0:
                print(primary_val)
                print(object_dataframe.schema)
                records = (
                    object_dataframe.select(primary_val)
                    .na.drop("any")
                    .rdd.flatMap(lambda x: x)
                    .collect()
                )
                dataframe = self.change_event_query(
                    sfdc_change_object=sfdc_parent_object, id_filter=records
                )

        return dataframe
