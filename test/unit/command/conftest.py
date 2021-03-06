#  Copyright (c) 2015-2016 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import os
import shutil

import pytest
import yaml


@pytest.fixture()
def molecule_file(tmpdir, request, molecule_vagrant_config):
    d = tmpdir.mkdir('molecule')
    c = d.join(os.extsep.join(('molecule', 'yml')))
    data = molecule_vagrant_config
    c.write(data)

    pbook = d.join(os.extsep.join(('playbook', 'yml')))
    data = [{'hosts': 'all', 'tasks': [{'command': 'echo'}]}]
    pbook.write(yaml.safe_dump(data))

    os.chdir(d.strpath)

    def cleanup():
        os.remove(c.strpath)
        shutil.rmtree(d.strpath)

    request.addfinalizer(cleanup)

    return c.strpath


@pytest.fixture
def patched_main(mocker):
    return mocker.patch('molecule.command.check.Check.main')


@pytest.fixture
def patched_logger_error(mocker):
    return mocker.patch('logging.Logger.error')


@pytest.fixture
def patched_print_info(mocker):
    return mocker.patch('molecule.util.print_info')
