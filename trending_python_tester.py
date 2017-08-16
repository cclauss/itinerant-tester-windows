#!/usr/bin/env python3
"""
    Update the repo's '.travis.yml' to trigger Travis CI to run flake8 tests on
    the top 25 GitHub Trending Python repos.

    Requires: pip3 install --update beautifulsoup4 github3.py requests lxml
        If lxml is not available, html5lib should be a workable substitute
"""

import bs4  # will require lxml or html5lib
import getpass
import requests
import webbrowser
from github3 import login as github3_login

username = getpass.getuser()  # Does local username == GitHub username?
print('Please enter the GitHub password for user: {}'.format(username))
gh = github3_login(username, getpass.getpass())

url = 'https://github.com/trending?l=Python'  # GitHub Trending top 25 repos

# these repos pass tests, have pull requests to pass tests, or are Py3 only
ignore = [
    '0x4D31/honeyLambda', '521xueweihan/HelloGitHub', 'Cisco-Talos/pyrebox',
    'ExplorerFreda/Structured-Self-Attentive-Sentence-Embedding',
    'Kaixhin/NoisyNet-A3C', 'PyCQA/flake8', 'StevenBlack/hosts',
    'UltimateHackers/Hash-Buster', 'aboul3la/Sublist3r',
    'ageitgey/face_recognition', 'airbnb/binaryalert',
    'andreiapostoae/dota2-predictor', 'anishathalye/seashells',
    'ansible/ansible', 'appsecco/bugcrowd-levelup-subdomain-enumeration',
    'astorfi/pythonic-automatic-email', 'astrofrog/mpl-scatter-density',
    'benjaminp/six', 'bethgelab/foolbox', 'channelcat/sanic',
    'chenjiandongx/pyecharts', 'cloudflare/receipt-printer',
    'csxeba/brainforge', 'dizballanze/django-eraserhead', 'django/django',
    'dmulholland/ivy', 'facebookresearch/DrQA', 'fchollet/keras',
    'friggog/tree-gen', 'home-assistant/home-assistant', 'iogf/crocs',
    'jadore801120/attention-is-all-you-need-pytorch',
    'jaesik817/visual-interaction-networks_tensorflow', 'jakubroztocil/httpie',
    'jisungk/RIDDLE', 'jmathai/elodie', 'jordanpotti/AWSBucketDump',
    'jrg365/gpytorch', 'lanpa/tensorboard-pytorch', 'leesoh/yams',
    'littlecodersh/ItChat', 'lmcinnes/umap', 'maciejkula/spotlight',
    'madeye/sssniff', 'meetshah1995/pytorch-semseg', 'metachris/logzero',
    'mitmproxy/mitmproxy', 'neufv/put-me-on-a-watchlist', 'openai/baselines',
    'pfnet-research/chainer-gan-lib', 'polyaxon/polyaxon', 'python/cpython',
    'quiltdata/quilt', 'reiinakano/xcessiv', 'reinforceio/tensorforce',
    'requests/requests', 'rg3/youtube-dl', 'sensepost/objection',
    'songrotek/Deep-Learning-Papers-Reading-Roadmap',
    'strizhechenko/netutils-linux', 'vinta/awesome-python',
    'vividvilla/csvtotable', 'worawit/MS17-010', 'yeleman/py3compat',
    'CQFIO/PhotographicImageSynthesis', 'hylang/hy', 'liangliangyy/DjangoBlog',
    'neozhaoliang/pywonderland', 'warner/magic-wormhole', 'bugcrowdlabs/HUNT',
    'fendouai/FaceRank', 'nottombrown/rl-teacher', 'TailorDev/Watson',
    'OmkarPathak/pygorithm', 'jamesob/tinychain', 'TorchCraft/StarData',
    'aaronduino/asciidots', 'nccgroup/demiguise', 'alexhude/uEmu',
    'codezjx/netease-cloud-music-dl', 'pytorch/pytorch', 'pennsignals/aptos',
    'brendan-rius/jupyter-c-kernel', 'vahidk/EffectiveTensorflow',
    'jiajunhuang/blog', 'apache/incubator-superset',
    'josephmisiti/awesome-machine-learning', 'bugcrowd/HUNT',
    'mil-tokyo/webdnn', 'chrisranderson/beholder', 'chainer/chainercv'
]

# the boilerplate content of the .travis.yml file
fmt = """language: python
env:
%s
python:
    - 2.7.13
    - 3.6
cache: pip
install:
    - pip install flake8  # pytest  # add other testing frameworks later
before_script:
    - URL=https://github.com/${REPO}
    - echo ; echo -n "flake8 testing of ${URL} on " ; python -V
    - git clone --depth=50 --branch=master ${URL} ~/${REPO}
    - cd ~/${REPO}
script:
    - echo stop the build if there are Python syntax errors or undefined names
    - echo ; echo -n "flake8 testing of ${URL} on " ; python -V
    - time flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics
    - echo exit-zero treats all errors as warnings.  The GitHub editor is 127 chars wide
    - time flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
notifications:
    on_success: change
    on_failure: change  # `always` will be the setting once code changes slow down

"""

# extract the repo names of GitHub's Top 25 Trending Python list
soup = bs4.BeautifulSoup(requests.get(url).content, 'lxml')  # or 'html5lib'
# 'python / cpython'
repos = soup.find('ol', class_="repo-list").find_all('a', href=True)
# 'python/cpython'
repos = (repo.text.strip().replace(' ', '') for repo in repos
         if '/' in repo.text and '://' not in repo.text)
# '    - REPO=python/cpython'  also strip out any repos that are in ignore list
repos = '\n'.join('    - REPO=' + repo for repo in repos
                  if 'shadowsocks' not in repo and repo not in ignore)
print(repos)
travis_text = fmt % repos

# log into GitHub and commit an update to .travis.yml which will trigger tests
travis = gh.repository(username, 'itinerant-tester').contents('/.travis.yml')
print(travis.update('trigger a new build', travis_text.encode('utf-8')))
webbrowser.open('https://travis-ci.org/{}/itinerant-tester'.format(username))
