import unittest, subprocess, sys, tempfile, os, shutil
from mock import patch
import tl


class TlTest(unittest.TestCase):
    @classmethod
    def setUpClass(letest):
        letest.workdir = tempfile.mkdtemp()
        tl.LogFile = os.path.join(letest.workdir, 'timelog.txt')
        # Prepare timelog file with existing tasks
        with open(tl.LogFile, 'w') as timelog:
            timelog.write("2015-03-13 13:21: lunch** :\n")
            timelog.write("2015-03-13 16:34: Upstream Ubuntu :  lp1415880\n")
            timelog.write("2015-03-13 17:45: L3 / L3 support :  SF7-openafs\n")
            timelog.write("2015-03-16 08:41: arrived\n")
            timelog.write("2015-03-16 09:57: Personal management :  email\n")
            timelog.write("2015-03-16 11:07: L3 / L3 support :  SF7-openafs\n")
            timelog.write("2015-03-16 11:11: L3 / L3 support :  SF801-kdump\n")

    @classmethod
    def tearDownClass(letest):
        shutil.rmtree(letest.workdir)

    def test_new(self):
        '''calling tl with only 'new' argument'''
        tl.log_activity('new', 'Arrived')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('Arrived'))

    def test_ua_entry(self):
        '''calling tl with a UA entry'''
        tl.log_activity('ua', 'This is one entry')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('L3 / L3 support : This is one entry'))

    def test_not_logged(self):
        '''calling tl with argument with two asterix'''
        tl.log_activity('lunch**')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('lunch**'))

    def test_absolutely_not_logged(self):
        '''calling tl with argument with three asterix'''
        tl.log_activity('lunch***')
        line = self._get_last_log_line().strip()
        self.assertTrue(line.endswith('lunch***'))

    def test_help(self):
        '''calling tl with ? to get help '''
        self.assertEqual(tl.show_help(), ("Categories : ['know', 'meet', "
                                          "'pers', 'skill', 'team', 'ua', "
                                          "'ubu', 'up']"))

    def test_select_tasks_out_of_range(self):
        '''calling tl with category only and giving out of range answer'''
        with patch('builtins.input', return_value='3'):
            tl.select_tasks('ua')
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF7-openafs\n2) SF801-kdump\nInvalid task number')
            self.assertEqual(tl.select_tasks('ua'), (None, None))

    def test_select_tasks_select_0(self):
        '''calling tl with category only and answering 0'''
        with patch('builtins.input', return_value='0'):
            tl.select_tasks('ua')
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF7-openafs\n2) SF801-kdump')
            self.assertEqual(tl.select_tasks('ua'), (None, None))

    def test_select_tasks_select_nothing(self):
        '''calling tl with category only and answering nothing'''
        with patch('builtins.input', return_value=''):
            tl.select_tasks('ua')
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, '1) SF7-openafs\n2) SF801-kdump')
            self.assertEqual(tl.select_tasks('ua'), (None, None))

    def test_select_tasks_select_valid(self):
        '''calling tl with category only and selecting first task'''
        with patch('builtins.input', return_value='1'):
            tl.select_tasks('ua')
            self.assertEqual(tl.select_tasks('ua'), ('ua', 'SF7-openafs'))

    def _get_last_log_line(self):
        with open(tl.LogFile, 'r') as timelog:
            for line in timelog:
                continue
        return(line)
