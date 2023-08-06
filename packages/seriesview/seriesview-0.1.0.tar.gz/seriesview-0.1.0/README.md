# seriesview

Create shareable, interactive views of timeseries using figurl.

### Hosting a backend server

A backend service implements the compute tasks needed to power the web GUI on a particular channel.

* Step 1: [Set up and run a kachery node on your computer](https://github.com/kacheryhub/kachery-doc/blob/main/doc/kacheryhub-markdown/hostKacheryNode.md)
* Step 2: [Create a new kachery channel](https://github.com/kacheryhub/kachery-doc/blob/main/doc/kacheryhub-markdown/createKacheryChannel.md) - be sure to authorize your own node as well as the [figurl](https://github.com/magland/figurl) node on this channel
  - Step 2b: Restart the kachery daemon after adding the channel for the changes to take effect
* Step 3: Install and set up seriesview (see below)
* Step 4: Run the seriesview backend (see below)
* Step 5: Create a seriesview model and open it using figurl

## SeriesView installation and setup

On the computer running the kachery daemon, install the python package:

```bash
pip install --upgrade seriesview
```

Set the FIGURL_CHANNEL environment variable to the name of the channel you set up on kachery

```bash
# You can put this in your ~/.bashrc
export FIGURL_CHANNEL=<name-of-your-kachery-channel>
```

## Running the SeriesView backend

To run the backend service:

```bash
seriesview-start-backend --channel <name-of-kachery-channel>
```

You can optionally specify a backend ID. See below for more details.

### Creating and viewing a SeriesView workspace

TODO

### Using a backend ID

When starting the backend service, you can optionally supply a backend ID, a secret string that can restrict access to the service:

```bash
seriesview-start-backend --channel <name-of-kachery-channel> --backend-id <secret-string>
```

Then, on the front-end, you can connect to your particular backend by setting the backend ID inside the figurl web app (use the channel button in the upper-right corner of the page).

If you are in a multi-user environment, you may want to have each user run their own backend, with different backend IDs. This could particularly work well if each user runs a backend on their own workstation, and all workstations connect to the same kachery daemon, with a shared kachery storage directory mounted on all workstations.
