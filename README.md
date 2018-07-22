Minnesota Candidate Scraper
===========================

[![CircleCI](https://circleci.com/gh/OpenTwinCities/mn_candidate_scraper.svg?style=svg)](https://circleci.com/gh/OpenTwinCities/mn_candidate_scraper)

A simple script that scrapes public candidate data from the
[Minnesota Secretary of State's website](https://candidates.sos.state.mn.us/)
and saves this data to a CSV.

## Install

1. Install virtualenv and virtualenvwrapper
2. `mkvirtualenv --python=python3 mn_candidate_scraper`
3. `pip install -r requirements.txt`

## Configuration

Copy `example.env` to `.env` and edit as needed. Optionally, you may specify the same environment variables in your shell.

If the required configuration is not available in `.env` or enviornment variables, the script will prompt you for them.


## Run

`python script.py`
