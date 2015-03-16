import unittest, subprocess, sys, tempfile, os
import tl


class TlTest(unittest.TestCase):
    @classmethod
    def setUpClass(letest):
        letest.workdir = tempfile.mkdtemp()
        LogFile = os.path.join(letest.workdir, 'timelog.txt')
        # Prepare timelog file with existing tasks
        with open(LogFile, 'w') as timelog:
            timelog.write("2015-03-13 13:21: lunch** :")
            timelog.write("2015-03-13 16:34: Upstream Ubuntu :  lp1415880")
            timelog.write("2015-03-13 17:45: L3 / L3 support :  SF79-openafs")
            timelog.write("2015-03-16 08:41: arrived")
            timelog.write("2015-03-16 09:57: Personal management :  email")
            timelog.write("2015-03-16 11:07: L3 / L3 support :  SF79-openafs")
            timelog.write("2015-03-16 11:11: L3 / L3 support :  SF80199-kdump")

    def test_new(self):
        '''calling tl with only new argument'''
        self.assertEqual(tl.log_activity('new'), 'Arrived')

    def test_not_logged(self):
        '''calling tl with argument with two asterix'''
        self.assertEqual(tl.log_activity('lunch**'), 'lunch**')

    def test_help(self):
        self.assertEqual(tl.show_help(), ("Categories : ['know', 'meet', "
                                          "'pers', 'skill', 'team', 'ua', "
                                          "'ubu', 'up']"))
