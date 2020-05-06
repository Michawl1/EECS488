"""
Author: Michael Thompson and Gareth Valentin
Date: 4/23/2020
About: This is alarm and alert file for the security system
"""
import yagmail
import playsound
import SecuritySystem.Resources.constants as constants


class Alarm:
    def __init__(self):
        self._mailing_list = []
        self._parse_mailing_list()

        self._yag = yagmail.SMTP("limunan96@gmail.com", "fhhiacwrumyjvoei")

    def _parse_mailing_list(self):
        with open(constants.MailPath) as f:
            line = f.readline()
            while line:
                self._mailing_list.append(line.strip())
                line = f.readline()

    def alert_mail(self):
        for receiver in self._mailing_list:
            self._yag.send(
                to=receiver,
                subject=constants.MailSubject,
                contents=constants.MailBody
            )

    @staticmethod
    def alert_sound():
        playsound.playsound(constants.AlarmSound)
