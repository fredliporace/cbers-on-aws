# CBERS on AWS

This repository describes the organization of China-Brazil Earth Resources Satellite (CBERS) data available on AWS and provide additional data and tools for its use.

Information about the CBERS program is available from INPE's site http://www.cbers.inpe.br/ (in Portuguese).

## Accessing CBERS data on AWS

All CBERS-4 MUX scenes are available from the start of the CBERS-4 mission. New images are pulled daily from INPE's catalog at http://www.dgi.inpe.br/catalogo/ and are converted to Cloud Optimized Geotiff format.

The data is organized in two s3 buckets, both located in the us-east-1 region.

### cbers-pds bucket

The data are organized using a directory structure based on each scene’s path, row and acquisition date. For instance, the files for CBERS-4 MUX scene CBERS_4_MUX_20160518_163_128_L4 are available in the following location: s3://cbers-pds/CBERS4/MUX/163/128/CBERS_4_MUX_20160518_163_128_L4/

The naming convention used for the files is  CBERS\_{N}\_{CAM}\_{YYYYMMDD}\_{PPP}\_{RRR}\_L{L}\_BAND{B}.{tif|xml}, where:
- N: mission.
- CAM: camera identification, currently MUX only.
- YYYYMMDD: acquisition date.
- PPP: path, see more information on reference grid below.
- RRR: row, see more information on reference grid below.
- L: processing level:
  - 2: system corrected image, expect some translation error.
  - 4: orthorectified with ground control points.
- B: band number
- tif|xml: tif for Geotiff files, xml for metadata files.

cbers-pds is a Requester Pays bucket, which means that you can access it freely within the us-east region, but you will incur charges if you download it elsewhere

### cbers-meta-pds bucket

The data are organized using a directory identical to the one shown above, the difference is that this bucket stores quicklooks for each scene. Each directory contains a large and a small quicklook, for instance:

- Large quicklook: s3://cbers-meta-pds/CBERS4/MUX/157/133/CBERS_4_MUX_20150607_157_133_L4/CBERS_4_MUX_20150607_157_133.jpg
- Small quicklook: s3://cbers-meta-pds/CBERS4/MUX/157/133/CBERS_4_MUX_20150607_157_133_L4/CBERS_4_MUX_20150607_157_133_small.jpeg

This bucket also provides a gzipped files describing all scenes at its root level.

s3://cbers-meta-pds/scene_list.gz or https://s3.amazonaws.com/cbers-meta-pds/scene_list.gz



