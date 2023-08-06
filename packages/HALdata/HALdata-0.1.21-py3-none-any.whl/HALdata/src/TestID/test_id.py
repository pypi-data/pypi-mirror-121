#!/usr/bin/env python

'''
MIT License
Copyright (c) 2021 Mikhail Hyde & Cole Crescas
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import snowflake.connector
import pandas as pd
import numpy as np
import json
import boto3
from botocore.exceptions import NoCredentialsError

class Hash_Key():
    def __init__(self):

        self.df = self.sfQuery(query = "SELECT * FROM NINJA_TESTING_BDP_DB_PROD.STAGE.TEST_ID_HASH;")
        self.df["TEST_ID_HASH"] = self.df["TEST_ID_HASH"].astype(str)

        filename = "aws_credentials.json"

        with open(filename, 'r') as f:
            aws_credentials = json.load(f)

        self.ACCESS_KEY = aws_credentials['ACCESS_KEY']
        self.SECRET_KEY = aws_credentials['SECRET_KEY']
        self.bucket = aws_credentials['bucket']

        self.s3 = boto3.client('s3', aws_access_key_id=self.ACCESS_KEY,
                            aws_secret_access_key=self.SECRET_KEY)

    def sfQuery(self, query=None):
        '''Basic Query Function: Provided a query and username, it will create an output dataframe of the queried data.
        '''

        print('Connecting to Snowflake\n')

        sql = query

        # Connection string
        con = snowflake.connector.connect(
                    user='CCRESCAS@SHARKNINJA.COM',
                    authenticator='externalbrowser',
                    account='sharkninja.us-east-1',
                    warehouse='NINJA_BDP_SMALL',
                    database='NINJA_TESTING_BDP_DB_PROD',
                    #schema='REPORTING'
        )

        print('Performing Query\n')

        cur = con.cursor()
        
        cur=cur.execute(sql)

        print('Writing to Dataframe\n')
        
        df = cur.fetch_pandas_all()
        
        print('Closing Cursor and Connection\n')
        cur.close()
        con.close()
        
        print(df.info())
        return df.copy(deep=True)


    def get_hash_table(self):
        """
        Gets hash table from snowflake 
        """

        #Query Snowflake and convert to string
        

        print(self.df.head(10))

        hash_input, filtered_df = Hash_Key.hash_error(self)

        #Looks through filtered df and selects next value
        hash_index = (filtered_df["TEST_ID_HASH"].astype(str).str[-3:]).sort_values(ascending=True)

        new_num = str((int(hash_index[-1:]) + 1)).zfill(3)

        #creates new hash key and asks for user input test description
        new_hash = hash_input + new_num
        new_desc = str(input("Please enter new test desc"))

        added_df = pd.DataFrame(data = [[new_hash, new_desc]], columns=["TEST_ID_HASH", "HUMAN_READABLE_DESC"]) 

        df = self.df.append(added_df, ignore_index=True)

        return df.copy(deep=True)

    def hash_error(self):
        """
        Error checking for hash key

        returns hash_input & filtered_df
        """

        #Asks for user input of first five characters
        hash_input = str(input("Please enter first 5 char of hash"))

        filtered_df = self.df[self.df['TEST_ID_HASH'].str.contains(hash_input)]


        if int(hash_input) < 0:
            print("Hash input cannot contain a negative number")
            Hash_Key.hash_error(self)
        
        elif len(hash_input) != 5:
            print("Initial Hash Key must be 5 characters")
            Hash_Key.hash_error(self)

        elif filtered_df.empty == True:
            print("No matches of this test ID, do you want to proceed?")
            proceed = str(input("Yes/No?   "))

            if proceed == "Yes":
                return hash_input, filtered_df
            elif proceed == "No":
                print("Thank you, Bye!")
                exit()
        else:
            return hash_input, filtered_df

    def upload_to_s3(self, file_name, local_file):
        '''
        Uploads a single file to the AWS s3 bucket.
        '''

        try:
            self.s3.upload_file(Filename=local_file, Bucket=self.bucket, Key=file_name) # (local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

