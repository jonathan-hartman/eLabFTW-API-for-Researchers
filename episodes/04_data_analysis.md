---
title: "Retrieving and Analyzing Data"
teaching: 45 # teaching time in minutes
exercises: 45 # exercise time in minutes
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I retrieve experiment data with Python?
- How can I analyze and visualize an attached data file?
- How can I upload analysis results to eLabFTW?
- How can I create and link experiments with Python?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Retrieve an experiment from eLabFTW using the Python package
- Retrieve an attached data file from an eLabFTW experiment using the Python package
- Use pandas and matplotlib to visualize downloaded data
- Create an experiment using the Python API client
- Upload analysis results to an experiment using the Python API client
- Link experiments using the Python API client

::::::::::::::::::::::::::::::::::::::::::::::::

## From an eLabFTW Experiment to a Plot

In the previous episodes, we created an experiment and attached `calibration.csv`.
Now we will reproduce the analysis workflow in an empty Jupyter Notebook:

1. Retrieve the experiment and its attached file.
2. Load the file into a pandas DataFrame.
3. Create and interpret a plot.
4. Upload the plot and an evaluation to eLabFTW.
5. Create a combined analysis experiment and link it to the source experiment.

:::::::::::::::::::::::::::::::::::::::: instructor

This section requires pre-created experiments in eLabFTW.

::::::::::::::::::::::::::::::::::::::::::::::::

## Import the Client and Analysis Libraries

The configured client, which we worked with in the previous episode, loads the API host and token from the `.env` file beside `client.py`. Don't forget to keep the token in the environment and do not place it in notebook cells or output - this is not as important if you are working on your personal computer, but is good to practice.

Again, since we are using a new notebook we import everything we need:

```python
import elabapi_python
from scripts.client import api_client
```

The first things we will do is run an experiment, creating data files to attach to the associated experiments in eLabFTW. 

To this end, experiments have already been created in eLabFTW through the UI - say, the planning took place there and the experimental parameters have been setup. We are going to use a super simples example where we grab a single experiment parameter from a set of experiments and run each measurement accordingly. If you check the eLabFTW UI, you will see three experiments with the category 'MEASUREMENT' titled 'Heating Test Run X', where X is a roman numeral. These each have an extra field called 'Laser Power', for where each experiment has a different value.

What we want to do:

1. Get this parameter from the experiments.
2. Run the three measurements, generating a file for each.
3. Attach these experiments back to the experiments.

First, let's get the experiments. To do so, we need the experiments api again. We can kind of guess from our previous coding experience that we will need an upload API. We can what that looks like by checking out the [examples/03-experiment-file-handling.py](https://github.com/elabftw/elabapi-python/blob/master/examples/03-experiment-file-handling.py) in the github repository.

```python
experiments_api = elabapi_python.ExperimentsApi(api_client)
uploads_api = elabapi_python.UploadsApi(api_client)
```

Note: run `%pip install elabapi_python` (or for any other packages) if needed.

We could get all experiments and then, as we just saw, which would work fine for our little team, but is not really efficient in reality. Luckily, the API allows us to query and this filter what it returns.

A quick check of the [swagger docs under **read experiments**](https://doc.elabftw.net/api/v2/#/Experiments/read-experiments) gives us information here. You can query terms, look experiments linked to specific other entries, and so on. We have a few options here, but let's keep ot simple and look for experiments with status 'Planning' and 'Heat Test Run' in title. We can get the ID through the browser UI by filtering by the sttus and checking the address bar.

```python
heating_experiments=experiments_api.read_experiments(q='Heating Test Run', status=80)
```

The return is a list of experiment objects. We can check how many it returned for a quick sanity check:

```python
len(heating_experiments)
````

Output:

```
3
````

We can also looks at the returned data:

```python
heating_experiments
````

Output:

```
[{'_date': '2026-10-30',
  'access_key': None,
  'body': None,
  'body_html': None,
  'canread': '{"teams": [], "users": [], "teamgroups": []}',
  'canwrite': '{"teams": [], "users": [], "teamgroups": []}',
  'category': 28,
  'category_color': 'bc0445',
  'category_title': 'Measurement',
  'comments': None,
  'compounds': None,
  'content_type': None,
  'created_at': '2026-10-30 10:11:57',
  'custom_id': None,
  'elabid': None,
  'exclusive_edit_mode': None,
  'experiments_links': None,
  'firstname': 'Nicole',
  'fullname': 'Nicole Parks',
  'has_attachment': None,
  'id': 128,
  'items_links': None,
  'lastchangeby': None,
  'lastname': 'Parks',
  'locked': 0,
  'locked_at': None,
  'lockedby': None,
  'metadata': None,
  'modified_at': '2026-10-30 13:05:48',
  'next_step': None,
  'orcid': None,
  'page': None,
  'rating': 0,
  'recent_comment': None,
  'related_experiments_links': None,
  'related_items_links': None,
  'sharelink': None,
  'state': 1,
  'status': 80,
  'status_color': '23135c',
  'status_title': 'Planning',
  'steps': None,
  'tags': None,
  'tags_id': '340,349',
  'team': 12,
  'template': -1,
  'timestamped': 0,
  'timestamped_at': None,
  'timestampedby': None,
  'title': 'Heating Test Run III',
  'type': None,
  'up_item_id': None,
  'uploads': None,
  'userid': 1},
 {'_date': '2026-10-30',
  'access_key': None,
  'body': None,
  'body_html': None,
  'canread': '{"teams": [], "users": [], "teamgroups": []}',
  'canwrite': '{"teams": [], "users": [], "teamgroups": []}',
  'category': 28,
  'category_color': 'bc0445',
  'category_title': 'Measurement',
  'comments': None,
  'compounds': None,
  'content_type': None,
  'created_at': '2026-10-30 10:09:19',
  'custom_id': None,
  'elabid': None,
  'exclusive_edit_mode': None,
  'experiments_links': None,
  'firstname': 'Nicole',
  'fullname': 'Nicole Parks',
  'has_attachment': None,
  'id': 127,
  'items_links': None,
  'lastchangeby': None,
  'lastname': 'Parks',
  'locked': 0,
  'locked_at': None,
  'lockedby': None,
  'metadata': None,
  'modified_at': '2026-10-30 13:05:48',
  'next_step': None,
  'orcid': None,
  'page': None,
  'rating': 0,
  'recent_comment': None,
  'related_experiments_links': None,
  'related_items_links': None,
  'sharelink': None,
  'state': 1,
  'status': 80,
  'status_color': '23135c',
  'status_title': 'Planning',
  'steps': None,
  'tags': None,
  'tags_id': '340,349',
  'team': 12,
  'template': -1,
  'timestamped': 0,
  'timestamped_at': None,
  'timestampedby': None,
  'title': 'Heating Test Run II',
  'type': None,
  'up_item_id': None,
  'uploads': None,
  'userid': 1},
 {'_date': '2026-10-30',
  'access_key': None,
  'body': None,
  'body_html': None,
  'canread': '{"teams": [], "users": [], "teamgroups": []}',
  'canwrite': '{"teams": [], "users": [], "teamgroups": []}',
  'category': 28,
  'category_color': 'bc0445',
  'category_title': 'Measurement',
  'comments': None,
  'compounds': None,
  'content_type': None,
  'created_at': '2026-10-30 09:55:43',
  'custom_id': None,
  'elabid': None,
  'exclusive_edit_mode': None,
  'experiments_links': None,
  'firstname': 'Nicole',
  'fullname': 'Nicole Parks',
  'has_attachment': None,
  'id': 126,
  'items_links': None,
  'lastchangeby': None,
  'lastname': 'Parks',
  'locked': 0,
  'locked_at': None,
  'lockedby': None,
  'metadata': None,
  'modified_at': '2026-10-30 13:05:25',
  'next_step': None,
  'orcid': None,
  'page': None,
  'rating': 0,
  'recent_comment': None,
  'related_experiments_links': None,
  'related_items_links': None,
  'sharelink': None,
  'state': 1,
  'status': 80,
  'status_color': '23135c',
  'status_title': 'Planning',
  'steps': None,
  'tags': None,
  'tags_id': '340,349',
  'team': 12,
  'template': -1,
  'timestamped': 0,
  'timestamped_at': None,
  'timestampedby': None,
  'title': 'Heating Test Run I',
  'type': None,
  'up_item_id': None,
  'uploads': None,
  'userid': 1}]
```

What we need to run our experiments is the laser power entry. There's a slight bug in the Python package as you may notice: metadata is returned as None - [this issue has been reported](https://github.com/elabftw/elabapi-python/issues/35), but it has not been fixed yet.

Normally, you would be able to use `heating_experiment.metadata` to pull out this piece of information. The code for iterating over the experiments and pulling it out would be:

```python
power_settings = []
for exp in heating_experiments:
    power_setting = exp.metadata.extra_fields["Laser Power"]
    power_settings.append(power_setting)
```

We've built a workaround. The returned data structure is a bit different, but that's fine. It works with the requests Python package and makes API requests directly without the eLabFTW API package:

```python
from scripts.client import API_HOST, API_KEY
import requests

heating_experiments_full = []

for exp in heating_experiments:
    exp_id = exp.get('id')
    endpoint = API_HOST + f'/experiments/{exp_id}'
    headers = {'Authorization': f'{API_KEY}'}
    response = requests.get(endpoint, headers=headers)
    heating_experiments_full.append(response.json())
```

Generally, it's good to know you have a lot of options to get where you need to be. Another possible workaround may have been, for example, to download the experiment as a JSON or ELN Format file and pull the info from there.

Now that we have our experiments, we can pull out the information we need. Again, we've saved the experiments as a list. In this case they are now a list of Python dictionaries instead of elabapi_python objects. We access the information a little differently. Let's look at a single experiment, accessing it by its index:

```python
heating_experiments_full[0]
```

```
[{'access_key': None,
  'body': '<p style="line-height:1;"><strong>Goal</strong>: Gain an understanding of salt water temperature behavior when heated with a "super laser". This will inidicate how to scale this experiment and threaten the world powers to bend to my every demand!</p>\n<p>The switch-off temperature is set to 100 by default (see fields below).\xa0</p>',
  'body_html': '<p style="line-height:1;"><strong>Goal</strong>: Gain an understanding of salt water temperature behavior when heated with a "super laser". This will inidicate how to scale this experiment and threaten the world powers to bend to my every demand!</p>\n<p>The switch-off temperature is set to 100 by default (see fields below).\xa0</p>',
  'canread': '{"teams": [], "users": [], "teamgroups": []}',
  'canread_base': 30,
  'canread_base_human': 'Only members of the team',
  'canread_is_immutable': 0,
  'canwrite': '{"teams": [], "users": [], "teamgroups": []}',
  'canwrite_base': 20,
  'canwrite_base_human': 'Only owner and admins',
  'canwrite_is_immutable': 0,
  'category': 28,
  'category_color': 'bc0445',
  'category_title': 'Measurement',
  'changelog': [{'created_at': '2026-10-30 13:05:48',
    'target': 'status',
    'content': '80',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:12:11',
    'target': 'metadata_Laser Power',
    'content': '125',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:12:03',
    'target': 'title',
    'content': 'Heating Test Run III',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:57',
    'target': 'created',
    'content': 'Experiment was created from <a href="experiments.php?mode=view&amp;id=127">Experiment #127</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:57',
    'target': 'tags',
    'content': 'Added tag "evil plan" with id: 340',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:57',
    'target': 'tags',
    'content': 'Added tag "miniature scale" with id: 349',
    'fullname': 'Nicole Parks',
    'userid': 1}],
  'comments': [],
  'compounds_links': [],
  'containers': [],
  'content_type': 1,
  'created_at': '2026-10-30 10:11:57',
  'created_from_id': 127,
  'created_from_type': 1,
  'created_from_type_human': 'experiment',
  'custom_id': None,
  'date': '2026-10-30',
  'elabid': '20261030-6bfdf255705718466183dde7c679bd7b782894e6',
  'events_start': None,
  'events_start_itemid': None,
  'exclusive_edit_mode': None,
  'experiments_links': [],
  'firstname': 'Nicole',
  'fullname': 'Nicole Parks',
  'hide_main_text': 0,
  'id': 128,
  'is_pinned': 0,
  'items_links': [{'entityid': 144,
    'title': 'Bluetooth Infrared Thermometer',
    'custom_id': None,
    'elabid': '20261020-d7ce38b251063e8904c615d74b35a2f6df9c2b2c',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 5,
    'category_title': '🔬Device',
    'category_color': 'f1af40',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 145,
    'title': 'Super Laser 2000 Mini',
    'custom_id': None,
    'elabid': '20261020-5c1b56e448e6a6ce88a7a3477236e6e2fbff6ee0',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 5,
    'category_title': '🔬Device',
    'category_color': 'f1af40',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 150,
    'title': 'Magnetic Stirbar (medium)',
    'custom_id': None,
    'elabid': '20261020-b0f1832f1ade1a572b44f307b65cc7ed1969cedf',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 44,
    'category_title': 'Equipment',
    'category_color': '503cb9',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 149,
    'title': 'Magnetic stirrer',
    'custom_id': None,
    'elabid': '20261020-758fc1098b020ca999de04b6693dd03791d7bd24',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 44,
    'category_title': 'Equipment',
    'category_color': '503cb9',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 147,
    'title': 'Beaker 500 ml',
    'custom_id': None,
    'elabid': '20261020-23d11e08cc207c83dead83a4be51f24839a366ae',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 41,
    'category_title': 'Glassware',
    'category_color': '75d5ff',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 146,
    'title': 'Polycarbonate Safety Chamber',
    'custom_id': None,
    'elabid': '20261020-9f6fe5fb55cf02e56ce7e9198cc44d561cfc057d',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 40,
    'category_title': 'PPE',
    'category_color': 'f3312f',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 148,
    'title': 'Salterwater 3.5%',
    'custom_id': None,
    'elabid': '20261020-6e1a3e6fba5070542baae447b54d23848390d39a',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 43,
    'category_title': 'Stock Solution',
    'category_color': 'a65d28',
    'status_id': None,
    'status_title': None,
    'status_color': None}],
  'last_signed_at': None,
  'last_signed_by': None,
  'lastchangeby': 1,
  'lastname': 'Parks',
  'locked': 0,
  'locked_at': None,
  'lockedby': None,
  'metadata': '{"extra_fields": {"Laser Power": {"type": "number", "unit": "W", "units": ["W"], "value": "125"}, "Switch-off Temperature": {"type": "number", "unit": "°C", "units": ["°C", "K"], "value": "100"}}}',
  'metadata_decoded': {'extra_fields': {'Laser Power': {'type': 'number',
     'unit': 'W',
     'units': ['W'],
     'value': '125'},
    'Switch-off Temperature': {'type': 'number',
     'unit': '°C',
     'units': ['°C', 'K'],
     'value': '100'}}},
  'modified_at': '2026-10-30 13:05:48',
  'next_step': None,
  'orcid': None,
  'page': 'experiments',
  'rating': 0,
  'recent_comment': None,
  'related_experiments_links': [],
  'related_items_links': [],
  'sharelink': 'https://elab.parks.web.gateway.ionos.coscine.dev/experiments.php?mode=view&id=128',
  'signature_count': 0,
  'state': 1,
  'status': 80,
  'status_color': '23135c',
  'status_title': 'Planning',
  'steps': [],
  'surrounding_bookers': [],
  'tags': 'evil plan|miniature scale',
  'tags_decoded': [{'id': 340, 'tag': 'evil plan', 'is_favorite': False},
   {'id': 349, 'tag': 'miniature scale', 'is_favorite': False}],
  'tags_id': '340,349',
  'team': 12,
  'team_name': 'FDMIII-API_2026_11',
  'timestamped': 0,
  'timestamped_at': None,
  'timestampedby': None,
  'title': 'Heating Test Run III',
  'type': 'experiments',
  'uploads': [],
  'userid': 1},
 {'access_key': None,
  'body': '<p style="line-height:1;"><strong>Goal</strong>: Gain an understanding of salt water temperature behavior when heated with a "super laser". This will inidicate how to scale this experiment and threaten the world powers to bend to my every demand!</p>\n<p>The switch-off temperature is set to 100 by default (see fields below).\xa0</p>',
  'body_html': '<p style="line-height:1;"><strong>Goal</strong>: Gain an understanding of salt water temperature behavior when heated with a "super laser". This will inidicate how to scale this experiment and threaten the world powers to bend to my every demand!</p>\n<p>The switch-off temperature is set to 100 by default (see fields below).\xa0</p>',
  'canread': '{"teams": [], "users": [], "teamgroups": []}',
  'canread_base': 30,
  'canread_base_human': 'Only members of the team',
  'canread_is_immutable': 0,
  'canwrite': '{"teams": [], "users": [], "teamgroups": []}',
  'canwrite_base': 20,
  'canwrite_base_human': 'Only owner and admins',
  'canwrite_is_immutable': 0,
  'category': 28,
  'category_color': 'bc0445',
  'category_title': 'Measurement',
  'changelog': [{'created_at': '2026-10-30 13:05:48',
    'target': 'status',
    'content': '80',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:12:21',
    'target': 'title',
    'content': 'Heating Test Run II',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:52',
    'target': 'body',
    'content': 'Depending on your instance configuration, the change in the body is possibly recorded in the revisions. <a href="revisions.php?type=experiments&amp;item_id=127">See revisions page.</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:49',
    'target': 'links',
    'content': 'Removed link to experiment: <a href="/experiments.php?mode=view&amp;id=126">Heating Test Run I</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:35',
    'target': 'metadata_Laser Power',
    'content': '100',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:11:30',
    'target': 'body',
    'content': 'Depending on your instance configuration, the change in the body is possibly recorded in the revisions. <a href="revisions.php?type=experiments&amp;item_id=127">See revisions page.</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:09:19',
    'target': 'created',
    'content': 'Experiment was created from <a href="experiments.php?mode=view&amp;id=126">Experiment #126</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:09:19',
    'target': 'tags',
    'content': 'Added tag "evil plan" with id: 340',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:09:19',
    'target': 'tags',
    'content': 'Added tag "miniature scale" with id: 349',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:09:19',
    'target': 'links',
    'content': 'Added link to experiment: <a href="/experiments.php?mode=view&amp;id=126">Heating Test Run I</a>',
    'fullname': 'Nicole Parks',
    'userid': 1}],
  'comments': [],
  'compounds_links': [],
  'containers': [],
  'content_type': 1,
  'created_at': '2026-10-30 10:09:19',
  'created_from_id': 126,
  'created_from_type': 1,
  'created_from_type_human': 'experiment',
  'custom_id': None,
  'date': '2026-10-30',
  'elabid': '20261030-83e2255949f2ef06e77b8120a7a623ac1a6b30e1',
  'events_start': None,
  'events_start_itemid': None,
  'exclusive_edit_mode': None,
  'experiments_links': [],
  'firstname': 'Nicole',
  'fullname': 'Nicole Parks',
  'hide_main_text': 0,
  'id': 127,
  'is_pinned': 0,
  'items_links': [{'entityid': 144,
    'title': 'Bluetooth Infrared Thermometer',
    'custom_id': None,
    'elabid': '20261020-d7ce38b251063e8904c615d74b35a2f6df9c2b2c',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 5,
    'category_title': '🔬Device',
    'category_color': 'f1af40',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 145,
    'title': 'Super Laser 2000 Mini',
    'custom_id': None,
    'elabid': '20261020-5c1b56e448e6a6ce88a7a3477236e6e2fbff6ee0',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 5,
    'category_title': '🔬Device',
    'category_color': 'f1af40',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 150,
    'title': 'Magnetic Stirbar (medium)',
    'custom_id': None,
    'elabid': '20261020-b0f1832f1ade1a572b44f307b65cc7ed1969cedf',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 44,
    'category_title': 'Equipment',
    'category_color': '503cb9',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 149,
    'title': 'Magnetic stirrer',
    'custom_id': None,
    'elabid': '20261020-758fc1098b020ca999de04b6693dd03791d7bd24',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 44,
    'category_title': 'Equipment',
    'category_color': '503cb9',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 147,
    'title': 'Beaker 500 ml',
    'custom_id': None,
    'elabid': '20261020-23d11e08cc207c83dead83a4be51f24839a366ae',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 41,
    'category_title': 'Glassware',
    'category_color': '75d5ff',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 146,
    'title': 'Polycarbonate Safety Chamber',
    'custom_id': None,
    'elabid': '20261020-9f6fe5fb55cf02e56ce7e9198cc44d561cfc057d',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 40,
    'category_title': 'PPE',
    'category_color': 'f3312f',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 148,
    'title': 'Salterwater 3.5%',
    'custom_id': None,
    'elabid': '20261020-6e1a3e6fba5070542baae447b54d23848390d39a',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 43,
    'category_title': 'Stock Solution',
    'category_color': 'a65d28',
    'status_id': None,
    'status_title': None,
    'status_color': None}],
  'last_signed_at': None,
  'last_signed_by': None,
  'lastchangeby': 1,
  'lastname': 'Parks',
  'locked': 0,
  'locked_at': None,
  'lockedby': None,
  'metadata': '{"extra_fields": {"Laser Power": {"type": "number", "unit": "W", "units": ["W"], "value": "100"}, "Switch-off Temperature": {"type": "number", "unit": "°C", "units": ["°C", "K"], "value": "100"}}}',
  'metadata_decoded': {'extra_fields': {'Laser Power': {'type': 'number',
     'unit': 'W',
     'units': ['W'],
     'value': '100'},
    'Switch-off Temperature': {'type': 'number',
     'unit': '°C',
     'units': ['°C', 'K'],
     'value': '100'}}},
  'modified_at': '2026-10-30 13:05:48',
  'next_step': None,
  'orcid': None,
  'page': 'experiments',
  'rating': 0,
  'recent_comment': None,
  'related_experiments_links': [],
  'related_items_links': [],
  'sharelink': 'https://elab.parks.web.gateway.ionos.coscine.dev/experiments.php?mode=view&id=127',
  'signature_count': 0,
  'state': 1,
  'status': 80,
  'status_color': '23135c',
  'status_title': 'Planning',
  'steps': [],
  'surrounding_bookers': [],
  'tags': 'evil plan|miniature scale',
  'tags_decoded': [{'id': 340, 'tag': 'evil plan', 'is_favorite': False},
   {'id': 349, 'tag': 'miniature scale', 'is_favorite': False}],
  'tags_id': '340,349',
  'team': 12,
  'team_name': 'FDMIII-API_2026_11',
  'timestamped': 0,
  'timestamped_at': None,
  'timestampedby': None,
  'title': 'Heating Test Run II',
  'type': 'experiments',
  'uploads': [],
  'userid': 1},
 {'access_key': None,
  'body': '<p style="line-height:1;"><strong>Goal</strong>: Gain an understanding of salt water temperature behavior when heated with a "super laser". This will inidicate how to scale this experiment and threaten the world powers to bend to my every demand!</p>\n<p>The switch-off temperature is set to 100 by default (see fields below).\xa0</p>',
  'body_html': '<p style="line-height:1;"><strong>Goal</strong>: Gain an understanding of salt water temperature behavior when heated with a "super laser". This will inidicate how to scale this experiment and threaten the world powers to bend to my every demand!</p>\n<p>The switch-off temperature is set to 100 by default (see fields below).\xa0</p>',
  'canread': '{"teams": [], "users": [], "teamgroups": []}',
  'canread_base': 30,
  'canread_base_human': 'Only members of the team',
  'canread_is_immutable': 0,
  'canwrite': '{"teams": [], "users": [], "teamgroups": []}',
  'canwrite_base': 20,
  'canwrite_base_human': 'Only owner and admins',
  'canwrite_is_immutable': 0,
  'category': 28,
  'category_color': 'bc0445',
  'category_title': 'Measurement',
  'changelog': [{'created_at': '2026-10-30 13:05:48',
    'target': 'status',
    'content': '80',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 13:05:25',
    'target': 'status',
    'content': '80',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 13:04:36',
    'target': 'status',
    'content': '47',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:12:38',
    'target': 'body',
    'content': 'Depending on your instance configuration, the change in the body is possibly recorded in the revisions. <a href="revisions.php?type=experiments&amp;item_id=126">See revisions page.</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:09:07',
    'target': 'title',
    'content': 'Heating Test Run I',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:09:01',
    'target': 'title',
    'content': 'Heating Test run I',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 10:08:35',
    'target': 'metadata_Laser Power',
    'content': '50',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 09:55:43',
    'target': 'created',
    'content': 'Experiment was created from <a href="templates.php?mode=view&amp;id=32">Experiment template #32</a>',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 09:55:43',
    'target': 'tags',
    'content': 'Added tag "evil plan" with id: 340',
    'fullname': 'Nicole Parks',
    'userid': 1},
   {'created_at': '2026-10-30 09:55:43',
    'target': 'tags',
    'content': 'Added tag "miniature scale" with id: 349',
    'fullname': 'Nicole Parks',
    'userid': 1}],
  'comments': [],
  'compounds_links': [],
  'containers': [],
  'content_type': 1,
  'created_at': '2026-10-30 09:55:43',
  'created_from_id': 32,
  'created_from_type': 3,
  'created_from_type_human': 'experiment template',
  'custom_id': None,
  'date': '2026-10-30',
  'elabid': '20261030-8fcae3ad5c21fa161382c8a181693d92c50d1921',
  'events_start': None,
  'events_start_itemid': None,
  'exclusive_edit_mode': None,
  'experiments_links': [],
  'firstname': 'Nicole',
  'fullname': 'Nicole Parks',
  'hide_main_text': 0,
  'id': 126,
  'is_pinned': 0,
  'items_links': [{'entityid': 144,
    'title': 'Bluetooth Infrared Thermometer',
    'custom_id': None,
    'elabid': '20261020-d7ce38b251063e8904c615d74b35a2f6df9c2b2c',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 5,
    'category_title': '🔬Device',
    'category_color': 'f1af40',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 145,
    'title': 'Super Laser 2000 Mini',
    'custom_id': None,
    'elabid': '20261020-5c1b56e448e6a6ce88a7a3477236e6e2fbff6ee0',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 5,
    'category_title': '🔬Device',
    'category_color': 'f1af40',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 150,
    'title': 'Magnetic Stirbar (medium)',
    'custom_id': None,
    'elabid': '20261020-b0f1832f1ade1a572b44f307b65cc7ed1969cedf',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 44,
    'category_title': 'Equipment',
    'category_color': '503cb9',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 149,
    'title': 'Magnetic stirrer',
    'custom_id': None,
    'elabid': '20261020-758fc1098b020ca999de04b6693dd03791d7bd24',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 44,
    'category_title': 'Equipment',
    'category_color': '503cb9',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 147,
    'title': 'Beaker 500 ml',
    'custom_id': None,
    'elabid': '20261020-23d11e08cc207c83dead83a4be51f24839a366ae',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 41,
    'category_title': 'Glassware',
    'category_color': '75d5ff',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 146,
    'title': 'Polycarbonate Safety Chamber',
    'custom_id': None,
    'elabid': '20261020-9f6fe5fb55cf02e56ce7e9198cc44d561cfc057d',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 40,
    'category_title': 'PPE',
    'category_color': 'f3312f',
    'status_id': None,
    'status_title': None,
    'status_color': None},
   {'entityid': 148,
    'title': 'Salterwater 3.5%',
    'custom_id': None,
    'elabid': '20261020-6e1a3e6fba5070542baae447b54d23848390d39a',
    'link_state': 1,
    'is_bookable': 0,
    'page': 'database.php',
    'type': 'items',
    'category_id': 43,
    'category_title': 'Stock Solution',
    'category_color': 'a65d28',
    'status_id': None,
    'status_title': None,
    'status_color': None}],
  'last_signed_at': None,
  'last_signed_by': None,
  'lastchangeby': 1,
  'lastname': 'Parks',
  'locked': 0,
  'locked_at': None,
  'lockedby': None,
  'metadata': '{"extra_fields": {"Laser Power": {"type": "number", "unit": "W", "units": ["W"], "value": "50"}, "Switch-off Temperature": {"type": "number", "unit": "°C", "units": ["°C", "K"], "value": "100"}}}',
  'metadata_decoded': {'extra_fields': {'Laser Power': {'type': 'number',
     'unit': 'W',
     'units': ['W'],
     'value': '50'},
    'Switch-off Temperature': {'type': 'number',
     'unit': '°C',
     'units': ['°C', 'K'],
     'value': '100'}}},
  'modified_at': '2026-10-30 13:05:25',
  'next_step': None,
  'orcid': None,
  'page': 'experiments',
  'rating': 0,
  'recent_comment': None,
  'related_experiments_links': [],
  'related_items_links': [],
  'sharelink': 'https://elab.parks.web.gateway.ionos.coscine.dev/experiments.php?mode=view&id=126',
  'signature_count': 0,
  'state': 1,
  'status': 80,
  'status_color': '23135c',
  'status_title': 'Planning',
  'steps': [],
  'surrounding_bookers': [],
  'tags': 'evil plan|miniature scale',
  'tags_decoded': [{'id': 340, 'tag': 'evil plan', 'is_favorite': False},
   {'id': 349, 'tag': 'miniature scale', 'is_favorite': False}],
  'tags_id': '340,349',
  'team': 12,
  'team_name': 'FDMIII-API_2026_11',
  'timestamped': 0,
  'timestamped_at': None,
  'timestampedby': None,
  'title': 'Heating Test Run I',
  'type': 'experiments',
  'uploads': [],
  'userid': 1}]
```

There is a `metadata` and a `metadata_decoded` key. We can quickly check what te differences are by using Python's built-in `type` function:

```python
type(heating_experiments_full[0]['metadata'])
```

Output:

```
str
````

```python
type(heating_experiments_full[0]['metadata_decoded'])
```

Output:

```
dict
```

Basically, `metadata_decoded` means the json-formatted string has already been decoded into a dictionary. This is what we need. Let's output that part so we know how to access the values needed:

```python
heating_experiments_full[0]['metadata_decoded']
```

Output

```
{'extra_fields': {'Laser Power': {'type': 'number',
   'unit': 'W',
   'units': ['W'],
   'value': '125'},
  'Switch-off Temperature': {'type': 'number',
   'unit': '°C',
   'units': ['°C', 'K'],
   'value': '100'}}}
```

We want the power value from the extra fields. Let's collect these in a list:

Now that we have the values, we can go ahead and use them. We've prepared a script that contains a function that generates some synthetic data and saves it as a CSV (see `scripts/generate_measurement.py`). Let's import this and run it for each experiment, e.g., every set of values. The function returns the path to the generated file, which we will save in a list so we can easily access each one in later steps.

```python
from scripts.generate_measurement import generate_measurement

measurement_files = []

for exp in heating_experiments_full:
    off_temp = exp['metadata_decoded']['extra_fields']['Switch-off Temperature']['value']
    laser_power = exp['metadata_decoded']['extra_fields']['Laser Power']['value']
    print(f"Running measurement with laser poser {laser_power} and shut-off temperature {off_temp}...")
    output_path = generate_measurement(power_w = float(laser_power), break_temp=float(off_temp))
    print(f"Output file saved to {output_path}")
    measurement_files.append(output_path)

```

If you check the output folder `output_data/`, you will see three files have been created.

Let's go ahead and attach these back to the experiment. Since we're in a new notebook, we have to create the upload client again.

```python
uploads_api = elabapi_python.UploadsApi(api_client)
for exp in heating_experiments_full:
    exp_id = exp['id']
    power = exp['metadata_decoded']['extra_fields']['Laser Power']['value']
    for file in measurement_files:
        if file.name.startswith(power):
            upload_client.post_upload(
                "experiments",
                exp_id,
                file=str(file),
    )
    
```

If you check your experiments in the UI, you should see your attached files.

::::::::::::::::::::::::::::::::::::: callout
Showing this in a Jupyter Notebook helps you better understand the single steps. However, as you may have noticed, this is really innefficient, e.g. it loops over the experiments list and gets the power variable twice. This would all be consolidated into a script. Here, we would create single functions for each step and so on. Then this could be run automatically, e.g., on a device computer, maybe one schedule that checks for new experimets entered throug the UI and then runs them for you and attached the output files for you to then check through the UI.
::::::::::::::::::::::::::::::::::::::::::::::::


We have not worked with Pandas or Matplotlib yet, but they are the most common Python libraries for data analysis and visualization. We will use them to load the CSV file and create a plot.

Also note, we use aliases for the libraries to make the code more concise. This is a common practice in Python, especially for frequently used libraries. `pd` is the standard alias for `pandas`, and `plt` is the alias for `matplotlib.pyplot`.

Next, we create the API clients we need:

```python
experiments_api = elabapi_python.ExperimentsApi(api_client)
uploads_api = elabapi_python.UploadsApi(api_client)
links_api = elabapi_python.LinksToExperimentsApi(api_client)
```

## Retrieve an Experiment

Use the experiment ID from the previous episode to retrieve your experiment. The response is an object containing the experiment metadata, body, links, and upload metadata.

```python
experiment_id = 94  # replace with the ID from the previous episode
experiment = experiments_api.get_experiment(experiment_id)

print(experiment.title)
print(experiment.body)
```

We use the uploads API to interact with the attached files. Inspect the attached files before downloading anything. This gives you a better idea of the structure of the returned data:

```python
uploads = uploads_api.read_uploads("experiments", experiment_id)

for upload in uploads:
    print(upload.id, upload.real_name, upload.comment)
```

The API distinguishes between upload metadata and the file contents. Select the measurement file and request its contents in binary format:

```python
measurement_upload = next(
    upload for upload in uploads if upload.real_name == "measurement.csv"
)

response = uploads_api.read_upload(
    "experiments",
    experiment_id,
    measurement_upload.id,
    format="binary",
    _preload_content=False,
)

measurement_path = Path("measurement.csv")
measurement_path.write_bytes(response.data)
```

::::::::::::::::::::::::::::::::::::: callout

The `_preload_content=False` argument is needed by this generated client when
downloading file content. Without `format="binary"`, the request returns upload information rather than the file itself.

::::::::::::::::::::::::::::::::::::::::::::::::

## Analyze and Visualize the Data

Load the downloaded CSV file and inspect its structure before plotting. This is where we will use Pandas to create a DataFrame from the CSV file. You can use the `parse_dates` argument to automatically convert the timestamp column to a datetime type:

```python
data = pd.read_csv("measurement.csv", parse_dates=["timestamp"])
data.head()
```

Now, we will use matplotlib (`plt`) to create a first plot of temperature over time:

```python
ax = data.plot(
    x="timestamp",
    y="temperature_c",
    marker="o",
    title="Temperature calibration",
    ylabel="Temperature (°C)",
    xlabel="Time",
    legend=False,
)
ax.grid(True)
plt.tight_layout()
plt.show()
```

Ask learners to write a short interpretation in a Markdown cell. For example:

> The temperature increases slightly during the measurement period, from 21.8
> °C to 22.1 °C. No abrupt changes are visible.

Save the plot so it can be attached to the source experiment:

```python
plot_path = Path("temperature_plot.png")
fig = ax.get_figure()
fig.savefig(plot_path, dpi=150, bbox_inches="tight")
```

## Upload the Analysis Result

The Python client uses the same upload endpoint as the cURL command from the
previous episode. The entity type is `experiments` and the entity ID is the
experiment receiving the file.

```python
notebook_path = Path("analysis_notebook.ipynb") # this notebook

uploads_api.post_upload(
    "experiments",
    experiment_id,
    file=str(plot_path),
    comment="Temperature calibration plot",
)

uploads_api.post_upload(
    "experiments",
    experiment_id,
    file=str(notebook_path),
    comment="Analysis notebook",
)
```

Refresh the upload list to verify the result:

```python
for upload in uploads_api.read_uploads("experiments", experiment_id):
    print(upload.real_name, upload.comment)
```

An evaluation can be added to the experiment body with `patch_experiment`:

```python
evaluation = """
<p>The temperature increased from 21.8 °C to 22.1 °C over the measurement period.
No abrupt changes are visible.</p>
"""

experiments_api.patch_experiment(
    experiment_id,
    body=elabapi_python.EntityEditable(bodyappend=evaluation),
)
```

## Create and Link an Analysis Experiment

Lets's create a separate experiment for the combined analysis. The API uses the `EntityEditable` model for experiment creation.

```python
analysis_experiment = elabapi_python.EntityEditable(
    title="Temperature calibration analysis",
    body="<p>Combined analysis of the calibration measurements.</p>",
)

experiments_api.post_experiment(body=analysis_experiment)
```

The create endpoint does not return a complete experiment object in every
client version. Retrieve the experiments again and use the ID of the newly
created experiment. In a real workflow, prefer the ID from the response
`Location` header when it is available.

```python
experiments = experiments_api.read_experiments()
for item in experiments[:5]:
    print(item.id, item.title)

```

Use the returned ID:

```python

analysis_experiment_id = 95  # replace with the newly created experiment ID
```

Link the analysis experiment to the source experiment. The direction is
important: here the source experiment receives a link to the analysis
experiment.

```python
links_api.post_entity_experiments_links(
    "experiments",
    experiment_id,
    analysis_experiment_id,
    body=elabapi_python.ExperimentsLinksSubidBody(action="link"),
)
```
<!-- TODO: add data files for mutiple experiments, retrieve, combine, plot, upload to new experiment, link to source experiments -->
Upload the combined plot or notebook to the analysis experiment:

```python
uploads_api.post_upload(
    "experiments",
    analysis_experiment_id,
    file=str(plot_path),
    comment="Combined analysis plot",
)
```

::::::::::::::::::::::::::::::::::::: challenge

Using a second experiment ID, adapt the code above to:

- retrieve its attached measurement file,
- create a plot with both measurements,
- write a short interpretation in a Markdown cell,
- upload the combined plot to a new analysis experiment, and
- link the two source experiments to that analysis experiment.

::::::::::::::::::::::::::::::::::::::: solution

Use `read_experiments` or the experiment IDs from the previous episodes to
select the source experiments. Retrieve each file with `UploadsApi`, load the
files into pandas, and combine them before plotting:

```python
experiment_ids = [94, 95]  # replace with the two source experiment IDs
frames = []

for source_id in experiment_ids:
    source_uploads = uploads_api.read_uploads("experiments", source_id)
    source_measurement = next(
        upload for upload in source_uploads if upload.real_name == "measurement.csv"
    )
    source_response = uploads_api.read_upload(
        "experiments",
        source_id,
        source_measurement.id,
        format="binary",
        _preload_content=False,
    )
    source_path = Path(f"measurement_{source_id}.csv")
    source_path.write_bytes(source_response.data)
    frame = pd.read_csv(source_path, parse_dates=["timestamp"])
    frame["experiment_id"] = source_id
    frames.append(frame)

combined = pd.concat(frames, ignore_index=True)
combined.plot(x="timestamp", y="temperature_c", by="experiment_id", marker="o")
plt.tight_layout()
plt.show()
```

The remaining steps are the same: create an analysis experiment, upload the
combined plot, and call `post_entity_experiments_links` for each source
experiment.


:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- The Python client can retrieve experiment metadata and attached files
- pandas can turn downloaded CSV data into a table ready for analysis
- matplotlib can visualize measurements and save plots for upload
- The API client can create experiments, upload files, and append evaluations
- Experiment links make the relationship between source data and analysis explicit

:::::::::::::::::::::::::::::::::::::::::::::::
