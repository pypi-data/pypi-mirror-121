# ------------------------------------------------------------------------------
# Copyright (c) 2015-2019 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------


import logging
import os
import sys
import threading
import requests

from requests.auth import HTTPBasicAuth

try:
    from pyupdater.core.uploader import BaseUploader
except ImportError:  # PyUpdater <3.0
    from pyupdater.uploader import BaseUploader

from pyupdater.utils.exceptions import UploaderError

log = logging.getLogger(__name__)


class NexusUploader(BaseUploader):

    name = 'Nexus'
    author = 'Pierre Chevalier'

    def init_config(self, config):
        self.url = os.environ.get(u'PYU_NEXUS_URL')
        if self.url is None:
            raise UploaderError('Missing PYU_NEXUS_URL',
                                expected=True)

        self.password = os.environ.get(u'PYU_NEXUS_PASSWORD')
        if self.password is None:
            raise UploaderError(u'Missing PYU_NEXUS_PASSWORD',
                                expected=True)
        self.username = os.environ.get(u'PYU_NEXUS_USERNAME')
        if self.username is None:
            raise UploaderError(u'Missing PYU_NEXUS_USERNAME',
                                expected=True)

        # Try to get bucket from env var
        self.repository = os.environ.get(u'PYU_NEXUS_REPOSITORY')
        repository = config.get(u'repository')

        # If there is a bucket name in the repo config we
        # override the env var
        if repository is not None:
            self.repository = repository

        # If nothing is set throw an error
        if self.repository is None:
            raise UploaderError(u'Repository name is not set',
                                expected=True)

        # Try to get bucket from env var
        self.directory = os.environ.get(u'PYU_NEXUS_DIRECTORY')
        directory = config.get(u'directory')
        
        # If there is a bucket name in the repo config we
        # override the env var
        if directory is not None:
            self.directory = directory

        # If nothing is set throw an error
        if self.directory is None:
            raise UploaderError(u'Directory name is not set',
                                expected=True)

        #self.session=requests.session()


    def set_config(self, config):
        repository = config.get('repository')
        repository = self.get_answer(
            'Please enter a repository name',
            default=repository
        )
        config['repository'] = repository

        directory = config.get('directory')
        directory = self.get_answer(
            'Please enter a directory name',
            default=directory
        )
        config['directory'] = directory

    def upload_file(self, filename):
        """Uploads a single file to S3

        Args:
            filename (str): Name of file to upload.

        Returns:
            (bool) Meanings::

                True - Upload Successful

                False - Upload Failed

        """

        try:

            auth=HTTPBasicAuth(self.username ,self.password)
            headers ={'accept': 'application/json'}
            files= (
                ('raw.directory',(None, self.directory)),
                ('raw.asset1',(os.path.basename(filename),open(filename,"rb"),"text/plain")),
                ('raw.asset1.filename',(None,os.path.basename(filename))),
            )
            response = requests.post(self.url+"/service/rest/v1/components?repository="+self.repository,
                headers=headers, auth=auth,files=files)

            log.debug('Uploaded {}'.format(filename))

            return response.ok

        except Exception as err:
            log.error('Failed to upload file')
            log.debug(err, exc_info=True)

            self._connect()

            return False
