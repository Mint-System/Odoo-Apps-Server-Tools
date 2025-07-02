import subprocess
import pymssql
import pytest
from datetime import datetime
from collections import defaultdict


SERVER = "localhost:1433"
DATABASE = "SchnittstellenDB"
USERNAME = "odoo"
PASSWORD = "uri%oodoJ2024"


@pytest.fixture(scope="module")
def mssql_conn():
    conn = pymssql.connect(
        server=SERVER,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = conn.cursor(as_dict=True)
    yield conn, cursor
    cursor.close()
    conn.close()

# columns in PPG Journal "STATUS","Belegnummer","Artikelid","Charge","Seriennummer","Menge","Richtung","Komplett","BzId", "Suchbegriff", "Row_Create_Time"

test_cases = [
    ("case_1", [
        (2, 'PC001', 0, '', '', 10, "4", 2, 100, 'TEST_PRODUCT1', '2023-01-01', '2023-01-02'),
        (2, 'PC002', 0, '', '', 5, "4", 1, 101, 'TEST_PRODUCT2',  '2023-01-01', '2023-01-02'),
    ]),
    ("case_2", [
        (2, 'DOC002', 0, 'SN002', 'CH002', 7, "4", 1, 200, 'TEST_PRODUCT3', '2023-01-01', '2023-01-02'),
        (2, 'DOC002', 0, 'SN002', 'CH002', 3, "4", 1, 201, 'TEST_PRODUCT4', '2023-01-01', '2023-01-02'),
    ]),
    ("case_3", [
        (2, 'DOC003', 0, 'SN003', 'CH003', 25, "4", 2, 300, 'TEST_PRODUCT5', '2023-01-01', '2023-01-02'),
    ]),
    ("case_4", [
        (1,"WH/PC/9991070",0,"","snuk-1001",1.0,"4",2,522868,"MOT.1021.010A.V002","Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"","snuk-2000",1.0,"4",1,522867,"MOT.1021.010A.V002","Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"LOT-24062025-1","",184.0,"4",1,522869,"icm.0320.F240.PQ.A","Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"LOT180625","",106.0,"4",1,522869,"icm.0320.F240.PQ.A","Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"","",219.0,"4",1,522866,"STS.00C8.IN01.60320.A","Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"","",1281.0,"4",1,522866,"STS.00C8.IN01.60320.A","Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"LOT180625","",247.0,"4",1,522870,"icm.0320.F240.PQ.A", "Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"lot160625","",163.0,"4",1,522870,"icm.0320.F240.PQ.A", "Nov 24 2024 12:11PM", ""),
        (1,"WH/PC/9991070",0,"LOT-RK200","",7.0,"4",1,522865,"MOT.1054.010A.V001","Nov 24 2024 12:11PM", ""),
    ]),
]



def nested_dict():
    return defaultdict(nested_dict)

@pytest.mark.parametrize("desc, test_rows", test_cases)
def test_ppg_journal_aggregation(mssql_conn, desc, test_rows):
    conn, cursor = mssql_conn

    # Extract Suchbegriff values

    bzid_values = set(row[8] for row in test_rows)
    print("bzid_values: ", bzid_values)

    placeholders = ', '.join(['%s'] * len(bzid_values))

    # Cleanup test data for all Suchbegriff values in this test case
    cursor.execute(f"DELETE FROM PPG_Journal WHERE BzId IN ({placeholders})", tuple(bzid_values))
    conn.commit()

    # Insert test data
    cursor.executemany("""
        INSERT INTO PPG_Journal (
            STATUS, Belegnummer, Artikelid, Charge, Seriennummer, Menge, Richtung, Komplett, BzId, Suchbegriff,
            Row_Create_Time, Row_Update_Time
        ) VALUES (%d, %s, %d, %s, %s, %d, %s, %d, %d, %s, %s, %s)
    """, test_rows)
    conn.commit()

    cursor.execute(f"""
        SELECT ID, BzId FROM PPG_Journal WHERE BzId IN ({placeholders}) ORDER BY BzId, ID
    """, tuple(bzid_values))

    rows = cursor.fetchall()

    expected = {}

    for row in test_rows:
        print("row in test rows: ", row)
        bzid = row[8]
        seriennummer = row[4]
        charge = row[3]
        menge = row[5]
        komplett = row[7]

        # Choose key or default
        key = seriennummer or charge or '__none__'
        group_key = (bzid, key)
        

        if group_key not in expected:
            expected[group_key] = {'menge': 0, 'max_komplett': 0}
        
        expected[group_key]['menge'] += menge
        expected[group_key]['max_komplett'] = max(expected[group_key]['max_komplett'], komplett)

    print("expected: ", expected)


    ids_by_bzid = defaultdict(list)
    for row in rows:
        print("row:", row)
        ids_by_bzid[row['BzId']].append(str(row['ID']))


    # Now run your query and assert per BzId
    for bzid in bzid_values:
        print("\n\nBzId", bzid)
        condition1 = f"WHERE BzId = '{bzid}'"

        # sql = f"""
        #     WITH CTE AS (
        #         SELECT BzId,
        #             Belegnummer,
        #             Seriennummer,
        #             Charge,
        #             Suchbegriff,
        #             Richtung,
        #             Row_Create_Time,
        #             Row_Update_Time,
        #             SUM(Menge) AS MengeErledigt,
        #             MAX(Komplett) AS MaxKomplett
        #         FROM PPG_Journal
        #         {condition1}
        #         GROUP BY BzId, Belegnummer, Seriennummer, Charge, Suchbegriff, Richtung, Row_Create_Time, Row_Update_Time
        #     )
        #     SELECT c.BzId,
        #         c.Belegnummer,
        #         c.Seriennummer,
        #         c.Charge,
        #         c.Suchbegriff,
        #         c.Richtung,
        #         c.Row_Create_Time,
        #         c.Row_Update_Time,
        #         c.MengeErledigt,
        #         c.MaxKomplett,
        #         STUFF(
        #                 (SELECT ', ' + CAST(ID AS VARCHAR)
        #                 FROM PPG_Journal
        #                 WHERE BzId = c.BzId
        #                 FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'),
        #                 1, 2, ''
        #         ) AS id_list
        #     FROM CTE c;
        # """
        # cursor.execute(sql)

        # sql = f"""
        #     WITH CTE AS (
        #         SELECT 
        #             BzId,
        #             ISNULL(NULLIF(COALESCE(Seriennummer, Charge), ''), '__none__') AS SerienOrCharge,
        #             SUM(Menge) AS MengeErledigt,
        #             MAX(Komplett) AS MaxKomplett
        #         FROM PPG_Journal
        #         WHERE BzId IN ({placeholders})
        #         GROUP BY BzId, ISNULL(NULLIF(COALESCE(Seriennummer, Charge), ''), '__none__')
        #     )
        #     SELECT * FROM CTE;
        # """

        non_aggregating_sql = f"""
            SELECT 
                BzId,
                Seriennummer, 
                Charge,
                Belegnummer,
                Suchbegriff,
                Richtung,
                Row_Create_Time,
                Row_Update_Time,
                Komplett
            FROM PPG_Journal
            {condition1}
        """

        cursor.execute(non_aggregating_sql)


        #result = cursor.fetchone()
        non_aggregating_result = cursor.fetchall()
        print("non_aggregating_result:", non_aggregating_result)



        sql = f"""
          WITH CTE AS (
                SELECT 
                    BzId,
                     CASE 
                        WHEN Seriennummer IS NOT NULL AND Seriennummer != '' THEN Seriennummer
                        WHEN Charge IS NOT NULL AND Charge != '' THEN Charge
                        ELSE '__none__'
                    END AS SerienOrCharge,
                    Belegnummer,
                    Suchbegriff,
                    Richtung,
                    Row_Create_Time,
                    Row_Update_Time,
                    SUM(Menge) AS MengeErledigt,
                    MAX(Komplett) AS MaxKomplett
                FROM PPG_Journal
                {condition1}
                GROUP BY 
                    BzId,
                    CASE 
                        WHEN Seriennummer IS NOT NULL AND Seriennummer != '' THEN Seriennummer
                        WHEN Charge IS NOT NULL AND Charge != '' THEN Charge
                        ELSE '__none__'
                    END,
                    Belegnummer,
                    Suchbegriff,
                    Richtung,
                    Row_Create_Time,
                    Row_Update_Time
            )
            SELECT 
                c.*,
                STUFF(
                    (
                        SELECT ', ' + CAST(ID AS VARCHAR)
                        FROM PPG_Journal j
                        WHERE 
                            j.BzId = c.BzId
                            AND ISNULL(NULLIF(COALESCE(j.Seriennummer, j.Charge), ''), '__none__') = c.SerienOrCharge
                            AND j.Belegnummer = c.Belegnummer
                            AND j.Suchbegriff = c.Suchbegriff
                            AND j.Richtung = c.Richtung
                            AND j.Row_Create_Time = c.Row_Create_Time
                            AND j.Row_Update_Time = c.Row_Update_Time
                        FOR XML PATH(''), TYPE
                    ).value('.', 'NVARCHAR(MAX)'),
                    1, 2, ''
                ) AS id_list
            FROM CTE c;
        """

        #cursor.execute(sql, tuple(bzid_values))
        cursor.execute(sql)


        #result = cursor.fetchone()
        result = cursor.fetchall()
        print("result:", result)

        for row in result:
            bzid = row['BzId']
            key = row['SerienOrCharge']
            group_key = (bzid, key)
            print("group key in sql result:", group_key)

            assert group_key in expected, f"Unexpected group {group_key} in SQL results"
            
            expected_menge = expected[group_key]['menge']
            expected_komplett = expected[group_key]['max_komplett']

            assert row['MengeErledigt'] == expected_menge, \
                f"MengeErledigt mismatch for {group_key}: expected {expected_menge}, got {row['MengeErledigt']}"

            assert row['MaxKomplett'] == expected_komplett, \
                f"MaxKomplett mismatch for {group_key}: expected {expected_komplett}, got {row['MaxKomplett']}"

        # assert result is not None
        # assert result['BzId'] == bzid
        # assert result['id_list'] == ', '.join(ids_by_bzid[bzid])
        # assert result['MengeErledigt'] == menge_by_bzid[bzid]
        # assert result['MaxKomplett'] == komplett_by_bzid[bzid]

    # Cleanup after
    cursor.execute(f"DELETE FROM PPG_Journal WHERE BzId IN ({placeholders})", tuple(bzid_values))
    conn.commit()



