
Now, let's say we've run these things 

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
