# Open Data Registry for CBERS on AWS

YAML for CBERS on AWS dataset, with comments

## Todo

- [ ] Finish project site (github page for now)
- [ ] Create SNS topic and include in YAML definition
- [ ] Include links to Sentinel and Landsat as related projects
- [ ] Make sure that tags are supported

## YAML file

```yaml
Name: CBERS on AWS
Description: |
  This project creates a S3 repository with imagery acquired
  by the China-Brazil Earth Resources Satellite (CBERS). The
  image files are recorded and processed by Instituto Nacional de Pesquisa
  Espaciais (INPE) and are converted to Cloud Optimized Geotiff
  format in order to optimize its use for cloud based applications.
  Currently the repository contains all CBERS-4 MUX images acquired since
  the start of the CBERS-4 mission.
Documentation: https://github.com/fredliporace/cbers
Contact: liporace@amskepler.com
UpdateFrequency: Daily
Tags:
  - cbers, satellite_imagery, check_if_tags_are_supported
License: https://creativecommons.org/licenses/by-sa/3.0/
Resources:
  - Description: CBERS imagery
    ARN: arn:aws:s3:::cbers-pds
    Region: us-east-1
    Type: S3 Bucket
DataATWork:
  - Description: Remote Pixel Viewer
    URL: https://viewer.remotepixel.ca
    AuthorName: Vincent Sarago
    AuthorURL: https://twitter.com/_VincentS_
```
