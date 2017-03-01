#!/usr/bin/env python

"""
gnss_metrics.txt is a file in the local directory that was produced by running

psql $DATABASE_URL -c "SELECT metrics_key_name FROM metrics_key_ids WHERE metrics_key_name LIKE 'GNSS%';" > gnss_metrics.txt

No descriptions for these. The following statement returned 0:

SELECT COUNT(metrics_key_description) from metrics_key_ids where metrics_key_name LIKE 'GNSS%';

This script formats a text file containing metrics names into yaml for
metrics_key_ids.yaml in hitl/schema
"""

def names_to_yaml(fname):
  '''From a file with one name per line, generate a yaml file that matches
  hitl/schema/metrics_key_ids.yaml
  '''
  with open(fname, 'r') as f:
    metric_names = f.readlines()

  metrics = []
  for metric_name in metric_names:
    metrics.append({
      'metrics_key_name': metric_name.strip(),
      'metrics_key_description': 'No description'
    })

  formatted_metrics = map(format_spacing, metrics)

  with open('gnss_metrics_key_ids.yaml', 'w') as f:
    f.write('\n'.join(formatted_metrics))

def format_spacing(metric):
  '''pyyaml writes like this

  - metrics_key_description: No description
  metrics_key_name: GNSS-Analysis/metrics/aggregates/distribution/spherical_error(m)/dgps/68%
  - metrics_key_description: No description
  metrics_key_name: GNSS-Analysis/metrics/aggregates/distribution/spherical_error(m)/dgps/50%

  But the program this needs to be fed to uses
  -
    metrics_key_name: "HeartbeatTest/metrics/heartbeat_dev_fail"
    metrics_key_description: "No description"
  -
    metrics_key_name: "HeartbeatTest/metrics/heartbeat_max_lag"
    metrics_key_description: "No description"

  Sadly, Stackoverflow seems to indicate this must be done by hand
  http://stackoverflow.com/questions/14228915/formatting-pyyaml-dump-output

  Parameters
  ----------
  metric: dict
    {'metrics_key_name': 'foo', 'metrics_key_description': 'bar'}
  '''
  template = '-\n  metrics_key_name: "{0}"\n  metrics_key_description: "{1}"'
  return template.format(metric['metrics_key_name'], metric['metrics_key_description'])


if __name__ == "__main__":
  names_to_yaml('gnss_metrics.txt')
