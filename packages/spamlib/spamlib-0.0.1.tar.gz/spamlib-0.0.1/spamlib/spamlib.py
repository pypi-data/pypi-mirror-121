import configparser
import smtplib
from progressbar import ProgressBar
from time import sleep

def startSpam(configList):
    config = configparser.ConfigParser()
    config.read(configList)
    i = 0
    login = config["SpamLib"]["login"].split('"')[1]
    password = config["SpamLib"]["password"].split('"')[1]



    smtpObj = smtplib.SMTP(config["SpamLib"]["smtpServer"].split('"')[1], config["SpamLib"]["smtpPort"].split('"')[1])
    smtpObj.starttls()
    smtpObj.login(login, password)

    def count_lines(filename, chunk_size=1<<13):
        with open(filename) as file:
            return sum(chunk.count('\n') + 1
                    for chunk in iter(lambda: file.read(chunk_size), ''))

    num_of_lines = count_lines(config["SpamLib"]["list"].split('"')[1])

    with open(config["SpamLib"]["list"].split('"')[1], "r") as f:
        emails = f.read().splitlines()

    pbar = ProgressBar(maxval=num_of_lines)
    pbar.start()
    mf = open(config["SpamLib"]["message"].split('"')[1], "r")
    for email in emails:
        smtpObj.sendmail(login,email,mf.read())
        sleep(1)
        pbar.update(i)
        i = i + 1
    pbar.finish()
    smtpObj.quit()
