#!/usr/bin/env python3
# Created by : Benjamin
# Project Script Name : Docker Monitoring Script
# This program Tool will read Information from Docker Containers on Local System

########################################################################################################################
# Imports

import os
import logging
import csv
import subprocess
import shlex


########################################################################################################################
# Function

def running_containers():
    # specify the encoding of the CSV data
    encoding = 'ascii'

    # Read Docker Information from Docker
    data = subprocess.Popen(shlex.split('docker ps --format " {{.Image}} {{.Status}} {{.Ports}} {{.ID}}"'),
                            stdout=subprocess.PIPE)

    # Converting output from subprocess to csv.reader object
    output = data.communicate()[0].decode(encoding)
    edits = csv.reader(output.splitlines(), delimiter=" ")

    # creating header for CSV file
    header = ['Image', 'Status', 'Ports', 'ID']

    # Create a CSV file in append mode
    with open('docker.csv', 'w+', newline='', encoding='utf-8') as my_file:
        # using csv.writer
        writer = csv.writer(my_file, delimiter=';')
        # write the Header in CSV
        writer.writerow(header)

        # Check each Row
        for row in edits:
            image_column = row[0]
            status_column = row[1]
            status2_column = row[2]
            status3_column = row[3]
            ports_column = row[-2]
            container_id = row[-1]

            # Create CSV format
            info_data = image_column,(status_column + ' ' + status2_column + ' ' + status3_column), ports_column, container_id
            # convert tuple to list
            new_csv_data = list(info_data)

            # Write a CSV docker file
            writer.writerows([new_csv_data])
            ids = [container_id]
            ############################################################################################################
            # create logs

            for item in ids:
                logging.root.handlers = []

                # Read Logs information containers
                log = os.popen(f'docker logs {item}')
                logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO,filename=f'{item}.log')

                # check log in different logging levels
                logging.debug(log)
                logging.info(log)
                logging.warning(log)
                logging.error(log)
                logging.exception(log)


#######################################################################################################################
# call main function
running_containers()
