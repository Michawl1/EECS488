"""
Author: Michael Thompson and Gareth Valentin
Date: 4/23/2020
About: This is alarm and alert file for the security system
"""
import yagmail
import playsound
import SecuritySystem.Resources.constants as constants


class Alarm:
    @staticmethod
    def _parse_mailing_list():
        mailing_list = []
        with open(constants.MailPath) as f:
            line = f.readline()
            while line:
                mailing_list.append(line.strip())
                line = f.readline()

        return mailing_list

    @staticmethod
    def alert_mail():
        yag = yagmail.SMTP("limunan96@gmail.com", "fhhiacwrumyjvoei")

        for receiver in Alarm._parse_mailing_list():
            print(receiver)
            yag.send(
                to=receiver,
                subject=constants.MailSubject,
                contents=constants.MailBody
            )

    @staticmethod
    def alert_sound():
        playsound.playsound(constants.AlarmSound)
