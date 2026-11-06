---
title: "Working with Data from eLabFTW"
teaching: 45 # teaching time in minutes
exercises: 45 # exercise time in minutes
---

:::::::::::::::::::::::::::::::::::::: questions

- How can I create a quick plot in Python?
- How can I add images to my eLabFTW entries?

::::::::::::::::::::::::::::::::::::::::::::::::

## Data Analysis Workflows

Let's imagine we had used an automated workflow in episode 05 to create the files. Everything ran in our absence and we have the individual output files attached to the experiments.

We can now keep going and add some more information to our experiments, such as a plot to quickly see the data.

We have not worked with Pandas or Matplotlib yet, but they are the most common Python libraries for data analysis and visualization. We will use them to load the CSV file and create a plot.

Also note, we use aliases for the libraries to make the code more concise. This is a common practice in Python, especially for frequently used libraries. `pd` is the standard alias for `pandas`, and `plt` is the alias for `matplotlib.pyplot`.

Since we're in a new notebook, we set everything up by creating the API clients we need:

```python
experiments_api = elabapi_python.ExperimentsApi(api_client)
uploads_api = elabapi_python.UploadsApi(api_client)
links_api = elabapi_python.LinksToExperimentsApi(api_client) #TODO CHECK IF WE NEED/MOVE
```

Let's access the one of our experiments and download the data file.

We keep using the `uploads_api` to interact with attached files. To ensure we have our experiment information, let's retrieve these again. We will filter by status again, but remember, we changed this to _Running_. The UI reminds us that this status has ID 47.

```python
heating_experiments = experiments_api.read_experiments(q='Heating Test Run', status = 47, scope=1)

```

Let's work with a single experiment and retrieve the data file. This is where we need the ID from the retrieved experiments. We will work with the first one in our list.

Check out the example in [examples/03-experiment-file-handling.py](https://github.com/elabftw/elabapi-python/blob/master/examples/03-experiment-file-handling.py). That gives us a function to work with. Let's copy and paste and then modify slightly:

```python
experiment = heating_experiments[0]

def download_matching_uploads_locally(exp): # added experiment
    # display id, name and comment of the uploaded files and download them locally
    for upload in uploads_api.read_uploads('experiments', exp.id): # match uploads_api spelling
        print(upload.id, upload.real_name, upload.comment, upload.state)
        # get and save file
        with open(upload.real_name, 'wb') as file: # edited file name variable to match real name
            # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
            file.write(uploads_api.read_upload('experiments', exp.id, upload.id, format='binary', _preload_content=False).data) # edited exp.id, match uploads_api spelling 
```

This will download all files attached to an experiment.

To call the function and download the file:

```python
download_matching_uploads_locally(experiment)
```

::::::::::::::::::::::::::::::::::::: callout

The `_preload_content=False` argument is needed by this generated client when
downloading file content. Without `format="binary"`, the request returns upload information rather than the file itself.

::::::::::::::::::::::::::::::::::::::::::::::::

## Visualize the Data

Using pandas, we can easily read in and plot the data. First we import pandas. We use the alias `pd` here, which is the standard way to import pandas. We read the CSV by file name using the `read_csv` method. Then, we can use `head` to view the first few lines of the dataframe.

```python
%pip install pandas # if needed
import pandas as pd

measurement_data = pd.read_csv("50_measurement_2026-11-05T11:27:07.281399.csv")
measurement_data.head()
```

Now, let's create a quick plot. Pandas uses the package matplotlib to do this.

```python
measurement_data.plot.scatter(x='time_s', y='temperature_C')
```

This is very basic. Let's add a title. We can also save he figure to a variable so we can keep working with it. In this case we want to save.

```python
ax = measurement_data.plot.scatter(x='time_s', y='temperature_C', title = 'Laser Power 50 W')
```

We now have the plot with the title. You can make all kinds of changes here, from axis labels to colors, but for a quick overview, it's sufficient. Let's save it.

```python
ax.figure.savefig("50w_temp_time_plot.png", dpi=300)
```

Attach to the experiment:

```python
uploads_api.post_upload('experiments', experiment.id, file="50w_temp_time_plot.png")
```

::::::::::::::::::::::::::::::::::::: challenge

Use the above snippets and function to write a code that

1. Retrieves all desired experiments
2. Plots and saves figures for each
3. Attaches the plot back to the experiment
4. Sets the experiment status to success

Hint: make a small modification to the `download_matching_uploads_locally` so you can retrieve the file name.

::::::::::::::::::::::::::::::::::::: solution
TODO
:::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::



::::::::::::::::::::::::::::::::::::: keypoints

- The eLabFTW Python API client allows you to retrieve all or specific files attached to an experiment
- pandas can turn downloaded CSV data into a table ready for analysis
- pandas has built-in matplotlib to visualize data and save plots

:::::::::::::::::::::::::::::::::::::::::::::::
