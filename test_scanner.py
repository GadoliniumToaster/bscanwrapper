"""Testing for filename"""
import scanner
import re

class TestFilename:
    """Testing Class"""

    def test_no_name_single(self):
        """Timestamp Single Scan"""
        x = scanner.filename()
        assert re.findall(r'\b\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.*', x)

    def test_no_name_batch(self):
        """Timestamp Batch Scan"""
        x = scanner.filename(batch=True)
        assert re.findall(r'\b\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_\d{3}.*', x)
