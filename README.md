# Clair Insight
Visual report of [Clair scanner](https://github.com/arminc/clair-scanner) results and white lists generator

## Clair scanner

Clair scanner is a vulnerabilities scanner for Docker images, it allows to scan images before publishing in the registry, 
it can be integrated in CI/CD pipelines or executed manually from CLI.

Clair scanner doesn't have an UI or a dashboard, the output is a static HTML report or a JSON file with the list of all discovered vulnerabilities.

For this reason Clair Insight allows you to load all JSON results created by Clair scanner and check vulnerabilities list quickly,
it includes libraries and severity filtering to analyze a portion of whole list.

With Clair Insight you can also generate a white list file, in YAML format, to load in Clair scanner and approve vulnerabilities,
a white list is useful when you want to skip any kind of vulnerability or a false positive. 

Before starting with Clair Insight you must configure Clair scanner.  
Please follow instruction on project documentation: https://github.com/arminc/clair-scanner

## How to run Clair Insight

Clair Insight requires two folders shared with Clair scanner, first one is where loads JSON result files exported at every scan and second one to export white list YAML files.

In my configuration example I consider these ones:

For JSON results files: `/opt/clair/json`  
For white lists YAML files: `/opt/clair/whitelists`

Change the paths as you prefer.  

If you don't want to share any folder with Clair scanner, you can use project `data/json` and `data/whitelists` folders and stores JSON file manually.

Before running Clair Insight you must configure the `.env` file, you can copy `env-example` and change values.

`.env`
```
DEBUG=False
SCAN_RESULTS_PATH=/opt/clair/json
WHITELISTS_EXPORT_PATH=/opt/clair/whitelists
SECRET_KEY=random-secret-key
CONTAINER_EXT_PORT=5005
``` 

Check or change container external port if you have another container or service running on the same port.

### Build image

You must build `clair-insight` Docker image:
```
make build
```
### Run container

When build process is done, run the container:
```
make run
```

### Application access

If everything has gone fine, you should be able to connect to `http://localhost:5005` and see Clair Insight UI.

## Clair scanner configuration

You must configure Clair scanner to export JSON results in the folder configured on Clair Insight,
in order to prevent file overwriting add a dynamic value like datetime to file name.
```
clair-scanner -r /opt/clair/json/scan-result-$(date '+%Y%m%d%H%M').json -c http://10.0.1.2:6060 --ip=10.0.1.3 debian:buster
```

In the next scans you may include exported white list file:
```
clair-scanner -w /opt/clair/whitelists/whitelist.yml -r /opt/clair/json/scan-result-$(date '+%Y%m%d%H%M').json -c http://10.0.1.2:6060 --ip=10.0.1.3 debian:buster
```

## Demo

If you want to have a look to Clair Insight, go to this link: https://clair-insight.particles.io/