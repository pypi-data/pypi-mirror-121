# A3D CLI #

Accessing the Axial3D apis from the command line

### Requirements

* Python 3.7, 3.8, 3.9

### Install

    pip install a3d-cli

#### Usage

Create an order:

    a3dcli create --config_file config.json --dicom_location ./path_to_dicoms/ --order-type 3DPrint --notes notes --surgery 'Surgery' --patient-gender M --patient-birth-year 2001 --catalogue-item 101 --required-date '10-08-2021'

Update an order

    a3dcli upload --config_file config.json --dicom_location ./path_to_dicoms/ --order_id 1000

View help:

```
a3dcli --help
usage: a3dcli [-h] --config_file CONFIG_FILE --order-type [ORDER_TYPES [ORDER_TYPES ...]] --catalogue-item-id [CATALOGUE_ITEM_ID] --surgery [SURGERY] --required-date [REQUIRED_DATE]
              --patient-gender [{M,F,U}] --patient-birth-year [BIRTH_YEAR] --notes [NOTES] [--base_url BASE_URL] [--verify] [--username USERNAME] [--password PASSWORD] [--order_id ORDER_ID] [--dicom_location DICOM_LOCATION] {create,upload}

Axial3D CLI (0.2.0)

positional arguments:
  {create,upload}
                        Create Order, Upload by order id

optional arguments:
  -h, --help            show this help message and exit
  --config_file CONFIG_FILE
                        a3dcli config file
  --order-type [ORDER_TYPES [ORDER_TYPES ...]]
                        Order Types
  --catalogue-item-id [CATALOGUE_ITEM_ID]
                        Catalogue Item
  --surgery [SURGERY]   Surgery
  --required-date [REQUIRED_DATE]
                        Required Date
  --patient-gender [{M,F,U}]
                        Gender
  --patient-birth-year [BIRTH_YEAR]
                        Gender
  --notes [NOTES]       Notes
  --base_url BASE_URL   Base url of axial3D API
  --verify
  --username USERNAME   axial3D account username
  --password PASSWORD   axial3D account password
  --order_id ORDER_ID   ID of the order
  --dicom_location DICOM_LOCATION
                        Path to DICOM files
```

### Dev requirements

* Poetry - https://python-poetry.org/
* Tox - https://tox.readthedocs.io/

### Build

    poetry build

### Testing

#### Unit tests

    poetry run pytest

#### Integration tests

    poetry run pytest --integration --integration-user USERNAME --integration-password PASSWORD --integration-url https://example.com

### Build

    poetry build

    > Building a3d-cli (0.1.0)
    > - Building sdist
    > - Built a3d-cli-0.1.0.tar.gz
    > - Building wheel
    > - Built a3d_cli-0.1.0-py3-none-any.whl