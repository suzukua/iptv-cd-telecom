name: iptv build

on:
  workflow_dispatch:
  #schedule:
    # - cron: "8 14 */2 * *"

env:
  TZ: Asia/Shanghai

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

#      - name: Set up WARP
#        uses: fscarmen/warp-on-actions@v1.1
#        with:
#          stack: dual   # Optional. Support [ ipv4, ipv6, dual ]. Default is dual.

      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r ./script/requirements.txt

      - name: Build home
        run: |
          python3 ./script/home.py

      - name: Commit
        run: |
          git config --global user.name 'suzukua_bot'
          git config --global user.email 'suzukua_bot'
          git add .
          git commit -am "Automated build"
          git push
