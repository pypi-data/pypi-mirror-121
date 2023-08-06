# FASTGenomics CLI

This package is a collection of scripts to manage your data on [FASTGenomics](https://beta.fastgenomics.org).

It can be installed via

```bash
pip install fastgenomics-cli
```

and contains the following tools

## FASTGenomics Upload

This script is used to upload files via the command line.

### Usage

```bash
fg-upload [-h] [-v] [-d DATASET] [-u USER] [-p PASSWORD] [-t TITLE] [-m] [--dataset_type DATASET_TYPE] [--url URL] file [file ...]

positional arguments:
  file                  the file(s) to be uploaded

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         more verbose output (default: False)
  -d DATASET, --dataset DATASET
                        add file to existing dataset with this id (default: None)
  -u USER, --user USER  your username (or email address) (default: None)
  -p PASSWORD, --password PASSWORD
                        your password (default: None)
  -t TITLE, --title TITLE
                        the title of the new dataset (default: None)
  -m, --metadata        upload files as metadata instead of expression data (default: False)
  --dataset_type DATASET_TYPE
                        the dataset type (default: None)
  --url URL             The platform url (default: https://beta.fastgenomics.org/)
```

## FASTGenomics CLI

This script is a generic command line interface for FASTGenomics.

### Usage

```bash
fg-cli -h
```

output

```bash
usage: fg-cli [-h] {login,logout,configure-aws,version,lfs,dataset} ...

 ______       _____ _______ _____                            _
|  ____/\    / ____|__   __/ ____|                          (_)
| |__ /  \  | (___    | | | |  __  ___ _ __   ___  _ __ ___  _  ___ ___
|  __/ /\ \  \___ \   | | | | |_ |/ _ \ '_ \ / _ \| '_ ` _ \| |/ __/ __|
| | / ____ \ ____) |  | | | |__| |  __/ | | | (_) | | | | | | | (__\__ \
|_|/_/    \_\_____/   |_|  \_____|\___|_| |_|\___/|_| |_| |_|_|\___|___/

Welcome to FASTGenomics CLI!
Version 0.12.0-c1

Here are the base commands:

optional arguments:
  -h, --help            show this help message and exit

FASTGenomics CLI:
  {login,logout,configure-aws,version,lfs,dataset}
                        Actions for FASTGenomics
    login               Log in to the platform.
    logout              Log out to remove access to the platform.
    configure-aws       Configure AWS for the platform
    version             Show the version of FASTGenomics CLI.
    lfs                 Manage Large File Storage (lfs)
    dataset             Manage datasets
```

### common

#### login

```bash
fg-cli login -h
```

output

```bash
usage: fg-cli login [-h] [-v] [-u USER] [-p PASSPHRASE] [-m {pat,password,bearer}] [--url URL]

Log in to the platform.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -u USER, --user USER  the platform user
  -p PASSPHRASE, --passphrase PASSPHRASE
                        the passphrase of platform user
  -m {pat,password,bearer}, --login_method {pat,password,bearer}
                        the login method 'pat' (personal access token), 'password' or 'bearer'. Default: pat
  --url URL             the url of the plattform. For Example: https://beta.fastgenomics.org
```

#### logout

```bash
fg-cli logout -h
```

output

```bash
usage: fg-cli logout [-h] [-v]

Log out to remove access to the platform.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

#### version

```bash
fg-cli version -h
```

output

```bash
usage: fg-cli version [-h] [-v]

Show the version of the cli client

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

### dataset

```bash
fg-cli dataset -h
```

output

```bash
usage: fg-cli dataset [-h] {get-types,get-type-details,create,upload-file,set-metadata,delete} ...

Group: fg dataset - Manage datasets.

positional arguments:
  {get-types,get-type-details,create,upload-file,set-metadata,delete}
    get-types           get available dataset types together with their name and description
    get-type-details    shows all editable fields for a dataset type
    create              create a dataset
    upload-file         upload files to dataset
    set-metadata        set the metadata for a dataset
    delete              delete a dataset

optional arguments:
  -h, --help            show this help message and exit
```

#### get dataset types

```bash
fg-cli dataset get-types -h
```

output

```bash
usage: fg-cli dataset get-types [-h] [-v]

get available dataset types together with their name and description

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

#### get dataset type details

```bash
fg-cli dataset get-type-details -h
```

output

```bash
usage: fg-cli dataset get-type-details [-h] [-v] [-m {brief,full}] [id]

shows all editable fields for a dataset type

positional arguments:
  id                    the id of the dataset type

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -m {brief,full}, --mode {brief,full}
                        description mode. Either "full" or "brief". Default "brief".
```

#### create a dataset

```bash
fg-cli dataset create -h
```

output

```bash
usage: fg-cli dataset create [-h] [-v] [-T TITLE] [--dataset_type DATASET_TYPE]

create a dataset

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -T TITLE, --title TITLE
                        the title of the dataset
  --dataset_type DATASET_TYPE
                        the dataset type. For example "cs-singlecell". To get an overview of available types use `fg-cli dataset get-types`
```

#### upload file to dataset

```bash
fg-cli dataset upload-file -h
```

output

```bash
usage: fg-cli dataset upload-file [-h] [-v] [-id ID] [-t [{primarydata,metadata}]] files [files ...]

upload files to dataset

positional arguments:
  files                 file names of the files to be uploaded

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -id ID                the id of the dataset
  -t [{primarydata,metadata}], --type [{primarydata,metadata}]
                        the type of the file 'primaryData' or 'metaData': Default: primaryData
```

#### set metadata of a dataset

```bash
fg-cli dataset set-metadata -h
```

output

```bash
usage: fg-cli dataset set-metadata [-h] [-v] [-id ID] metadata

set the metadata for a dataset

positional arguments:
  metadata       the metadate to set. Use @<filename> to provide the data by file or '{ json }'. Depending on your system you might have to escape quotes accordingly.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
  -id ID         the id of the dataset
```

set metadata by json string

```bash
fg-cli dataset set-metadata -id dataset-7463ed6a051b8557c7a03b33214e504e  -d '{ "title": "new title" }'
```

set metadata by file 'meta.json' containing the json

```bash
fg-cli dataset set-metadata -id dataset-7463ed6a051b8557c7a03b33214e504e  -d "@meta.json"
```

#### delete dataset

```bash
fg-cli dataset delete -h
```

output

```bash
usage: fg-cli dataset delete [-h] [-v] id

delete a dataset

positional arguments:
  id             the id of the dataset

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

### large file storage (lfs)

```bash
fg-cli lfs -h
```

output

```bash
usage: fg-cli lfs [-h] [-v] {create,get-url} ...

Group: fg lfs - Manage platform Large File Storage (lfs)

positional arguments:
  {create,get-url}
    create          Create and upload a large file storage
    get-url         Get a download url

optional arguments:
  -h, --help        show this help message and exit
  -v, --verbose     Activate verbose output
```

#### create lfs

```bash
fg-cli lfs create -h
```

output

```usage: fg-cli lfs create [-h] [-v] [-z [ZIP_FILENAME]] [-P [ZIP_PASSWORD]] -r RECIPIENT_EMAIL [-T [TITLE]] [--provider [{azure,aws}]] [--skip-compression] files_or_directory [files_or_directory ...]

Create and upload a large file storage

positional arguments:
  files_or_directory    file names or directory to be compressed

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Activate verbose output
  -z [ZIP_FILENAME], --zip-filename [ZIP_FILENAME]
                        name of the zip file
  -P [ZIP_PASSWORD], --zip-password [ZIP_PASSWORD]
                        password for the zip file. if omitted a password will be generated.
  -r RECIPIENT_EMAIL, --recipient-email RECIPIENT_EMAIL
                        the email address used in the platform of the recipient
  -T [TITLE], --title [TITLE]
                        the title of the dataset containing the uploaded data
  --provider [{azure,aws}]
                        the provider to be used 'azure' or 'aws'. Default: azure)
  --skip-compression    Skip the compression
```

#### get url of lfs

```bash
fg-cli lfs get-url -h
```

output

```bash
usage: fg-cli lfs get-url [-h] [-v] id access_token

Get a download url

positional arguments:
  id             the id of the storage
  access_token   the access token

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```

#### configure AWS

```bash
fg-cli configure-aws -h
```

output

```bash
usage: fg-cli configure-aws [-h] [-v]

Configure AWS for the platform

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Activate verbose output
```
