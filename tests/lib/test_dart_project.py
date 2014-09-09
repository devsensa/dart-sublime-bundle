import sublime

from tempfile import TemporaryDirectory
from unittest import mock
import os
import unittest

from Dart.lib.pub_package import PubspecFile
from Dart.lib.pub_package import DartProject


VALID_PUBSPEC_CONTENT = '''name: foo
version: 0.10
'''

VALID_PUBSPEC_LOCK_CONTENT = '''# Generated by pub
# See http://pub.dartlang.org/doc/glossary.html#lockfile
packages: {}
'''


class Test_PubspecFile(unittest.TestCase):
    def testInitCanFail(self):
        p = PubspecFile.from_path('???')
        self.assertEqual(p, None)

    def testInitCanSucceed(self):
        with TemporaryDirectory() as d:
            fname = os.path.join(d, 'pubspec.yaml')
            with open(fname, 'wt') as f:
                f.write(VALID_PUBSPEC_CONTENT)
            p = PubspecFile.from_path(fname)
            self.assertEqual(fname, p.path)

    def testCanFindParent(self):
        with TemporaryDirectory() as d:
            fname = os.path.join(d, 'pubspec.yaml')
            with open(fname, 'wt') as f:
                f.write(VALID_PUBSPEC_CONTENT)
            p = PubspecFile.from_path(fname)
            self.assertEqual(d, p.parent)

    def testCanFailToRetrievePubspecLock(self):
        with TemporaryDirectory() as d:
            fname = os.path.join(d, 'pubspec.yaml')
            with open(fname, 'wt') as f:
                f.write(VALID_PUBSPEC_CONTENT)
            p = PubspecFile.from_path(fname)
            self.assertEqual(None, p.get_pubspec_lock())

    def testCanRetrievePubspecLock(self):
        with TemporaryDirectory() as d:
            pubspec_fname = os.path.join(d, 'pubspec.yaml')

            with open(pubspec_fname, 'wt') as f:
                f.write(VALID_PUBSPEC_CONTENT)

            pubspec_lock_fname = os.path.join(d, 'pubspec.lock')
            with open(pubspec_lock_fname, 'wt') as f:
                f.write(VALID_PUBSPEC_LOCK_CONTENT)

            p = PubspecFile.from_path(pubspec_fname)
            self.assertEqual(pubspec_lock_fname, p.get_pubspec_lock().path)


class Test_DartProject(unittest.TestCase):
    def setUp(self):
        self.d = TemporaryDirectory()
        fname = os.path.join(self.d.name, 'pubspec.yaml')
        with open(fname, 'wt') as f:
            f.write(VALID_PUBSPEC_CONTENT)
        self.p = PubspecFile.from_path(fname)

    def tearDown(self):
        self.d.cleanup()

    def testInitCanFail(self):
        p = DartProject.from_path('???')
        self.assertEqual(p, None)

    def testInitCanSucceed(self):
        p = DartProject.from_path(self.d.name)
        self.assertEqual(self.d.name, p.pubspec.parent)
