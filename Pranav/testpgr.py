#!/usr/bin/env python3

import os
import unittest
from pgr import download_remote, save_file, serve_dir


TESTDIR = 'tests'

class TestPgr(unittest.TestCase):

    # Not fully implemented
    def __init__(self, *args, **kwargs):
        super(TestPgr, self).__init__(*args, **kwargs)

        if not os.path.isdir(TESTDIR):
            os.mkdir(TESTDIR)


    def test_download_webpage_redirected(self):
        url = 'https://google.com/'
        content, name = download_remote(url)

        # Check redirected webpage download
        self.assertEqual(name, ('index.html'))
        self.assertEqual(content[:9], b'<!doctype')


    def test_download_file_redirected(self):
        url = 'https://a1.pranavp.com.np/0:down/Getting%20started'

        # Check redirected file download
        self.assertEqual(download_remote(url)[1], ('Getting%20started'))


    def test_save_file_default(self):
        dummy_content = b'downloaded'
        dummy_filename = 'test.save'
        dummy_out = save_file(dummy_content, dummy_filename)

        # Check save directory
        self.assertEqual(dummy_out, '.')
        # Check saved filename
        self.assertEqual(os.path.isfile(dummy_filename), True)

        # Check saved content
        with open(dummy_filename, 'r') as f:
            saved_content = f.readline()
            self.assertEqual(saved_content, dummy_content.decode())

        # Delete created files
        os.remove(dummy_filename)



if __name__ == '__main__':
    unittest.main()
