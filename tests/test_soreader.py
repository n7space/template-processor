"""
Tests for SOReader class
"""

import pytest
from pathlib import Path
from templateprocessor.soreader import SOReader
from templateprocessor.so import SystemObjectType, SystemObject


class TestSOReader:
    """Test cases for SOReader class."""

    # Assuming the data directory is at the workspace root
    @staticmethod
    def get_test_data_file(filename: str) -> Path:
        """Get the path to a test data file."""
        return Path(__file__).parent.parent / "data" / filename

    def test_read_simple_values_from_csv(self):
        """Test reading the events.csv file. Basic file."""
        # Prepare
        reader = SOReader()
        csv_file = self.get_test_data_file("events.csv")
        assert csv_file.exists()

        # Read
        so_type = reader.read(csv_file)

        # Verify structure
        assert isinstance(so_type, SystemObjectType)

        # Verify property names (headers)
        assert len(so_type.property_names) == 4
        assert "ID" in so_type.property_names
        assert "Name" in so_type.property_names
        assert "Auxilary data" in so_type.property_names
        assert "Severity" in so_type.property_names

        # Verify instances were parsed
        assert len(so_type.instances) == 12

        # Check first instance
        first_instance = so_type.instances[0]
        assert isinstance(first_instance, SystemObject)
        assert first_instance.values["ID"] == "0"
        assert first_instance.values["Name"] == "e00 null event"
        assert first_instance.values["Auxilary data"] == "Empty"
        assert first_instance.values["Severity"] == "informative"

        # Check last instance
        last_instance = so_type.instances[11]
        assert isinstance(last_instance, SystemObject)
        assert last_instance.values["ID"] == "22"
        assert last_instance.values["Name"] == "e22 jettison parachute"
        assert last_instance.values["Auxilary data"] == "Empty"
        assert last_instance.values["Severity"] == "informative"

    def test_read_complex_values_from_csv(self):
        """Test reading the parameters.csv file. Contains complex values."""
        # Prepare
        reader = SOReader()
        csv_file = self.get_test_data_file("parameters.csv")
        assert csv_file.exists()

        # Read
        so_type = reader.read(csv_file)

        # Verify structure
        assert isinstance(so_type, SystemObjectType)

        # Verify property names
        assert "ID" in so_type.property_names
        assert "Name" in so_type.property_names
        assert "PTC" in so_type.property_names
        assert "PFC" in so_type.property_names
        assert "Memory Address" in so_type.property_names
        assert "Memory Name" in so_type.property_names
        assert "Default Sampling Interval" in so_type.property_names
        assert "Default Sampling Interval Value" in so_type.property_names
        assert "Default Value" in so_type.property_names
        assert "Default Value Type" in so_type.property_names

        # Verify instances
        assert len(so_type.instances) == 14

        # Find specific parameter
        param_instances = [
            inst
            for inst in so_type.instances
            if inst.values.get("Name") == "op01 current velocity horizontal"
        ]
        assert len(param_instances) == 1
        param = param_instances[0]
        assert param.values["ID"] == "1"
        assert param.values["PTC"] == "5"
        assert param.values["PFC"] == "1"
        assert param.values["Memory Address"] == "0"
        assert param.values["Memory Name"] == "ram memory"
        assert param.values["Default Sampling Interval"] == "Time Interval"
        assert (
            param.values["Default Sampling Interval Value"]
            == "Default Sampling Interval#{ t-field {day 0, milisecond 100, submilisecond 0}}"
        )
        assert (
            param.values["Default Value"]
            == "Default Value Type#{ field-data '00000000'H }"
        )
        assert param.values["Default Value Type"] == "Parameter Value"

    def test_read_multiline_values_from_csv(self):
        """Test reading the housekeeping.csv file. Contains multiline values."""
        # Prepare
        reader = SOReader()
        csv_file = self.get_test_data_file("housekeeping.csv")
        assert csv_file.exists()

        # Read
        so_type = reader.read(csv_file)

        # Verify structure
        assert isinstance(so_type, SystemObjectType)
        assert len(so_type.property_names) > 0
        assert len(so_type.instances) > 0

        # Verify property names
        assert "ID" in so_type.property_names
        assert "Name" in so_type.property_names
        assert "Collection Interval" in so_type.property_names
        assert "Simply Commuted Parameters" in so_type.property_names
        assert "Super Commuted Parameter Sets" in so_type.property_names
        assert "Periodic Generation Action Status" in so_type.property_names
        assert "Simply Commuted Parameters Value" in so_type.property_names
        assert "Super Commuted Parameter Sets Value" in so_type.property_names
        assert "Periodic Generation Action Status Value" in so_type.property_names

        # Verify instances
        assert len(so_type.instances) == 2

        # Check first instance
        first_instance = so_type.instances[0]
        assert isinstance(first_instance, SystemObject)
        assert first_instance.values["ID"] == "1"
        assert first_instance.values["Name"] == "hk01 status"
        assert first_instance.values["Collection Interval"] == "10"
        assert first_instance.values["Simply Commuted Parameters"] == "Parameter IDs"
        assert (
            first_instance.values["Super Commuted Parameter Sets"]
            == "Super Commuted Parameter Sets System Object Value"
        )
        assert (
            first_instance.values["Periodic Generation Action Status"]
            == "Periodic Generation Action Status"
        )
        assert (
            first_instance.values["Simply Commuted Parameters Value"]
            == """Simply Commuted Parameters#{ field-data { 
op51-mission-phase,
op21-parachute-status,
op31-thruster-1-power, 
op32-thruster-2-power, 
op33-fuel-left
} }"""
        )
        assert (
            first_instance.values["Super Commuted Parameter Sets Value"]
            == "Super Commuted Parameter Sets#{ field-data {  } }"
        )
        assert (
            first_instance.values["Periodic Generation Action Status Value"]
            == "Periodic Generation Action Status#enabled"
        )

    def test_read_string(self):
        """Test reading CSV from a string."""
        # Prepare
        reader = SOReader()
        csv_content = """ID;Name;Type
1;Item One;Type A
2;Item Two;Type B"""

        # Read
        so_type = reader.read_string(csv_content)

        # Verify
        assert isinstance(so_type, SystemObjectType)
        assert len(so_type.property_names) == 3
        assert so_type.property_names == ["ID", "Name", "Type"]
        assert len(so_type.instances) == 2
        assert so_type.instances[0].values["ID"] == "1"
        assert so_type.instances[1].values["Name"] == "Item Two"

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        reader = SOReader()
        with pytest.raises(FileNotFoundError):
            reader.read("nonexistent.csv")

    def test_custom_delimiter(self):
        """Test reading CSV with custom delimiter."""
        # Prepare
        reader = SOReader()
        csv_content = """ID,Name,Value
1,First,100
2,Second,200"""

        # Read with comma delimiter
        so_type = reader.read_string(csv_content, delimiter=",")

        # Verify
        assert len(so_type.property_names) == 3
        assert len(so_type.instances) == 2
        assert so_type.instances[0].values["ID"] == "1"
        assert so_type.instances[1].values["Value"] == "200"
