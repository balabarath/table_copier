# Postgresql Table Copier

Simple python utility for copying all the records available in the postgres database table to another postgres  database table.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need python installed in your machine.

### Installing

1) Clone this project.
2) Configure the config.yaml file
3) Execute the table_copier.py as shown below

```
./table_copier.py
```

### Note

Set the 'delete_destination_db_tables_record_before_copy' property to 'true' to delete all
 the records in the destination table before copy


## Authors

* **Balasubramanian Naagarajan** - (https://github.com/balabarath)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details
