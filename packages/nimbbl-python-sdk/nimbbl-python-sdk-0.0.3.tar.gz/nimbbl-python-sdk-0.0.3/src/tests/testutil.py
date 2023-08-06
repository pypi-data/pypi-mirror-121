import os

def mock_file(filename):
        if not filename:
            return ''
        file_dir = os.path.dirname(__file__)
        file_path = "{}/mocks/{}.json".format(file_dir, filename)
        with open(file_path) as f:
            mock_file_data = f.read()
        return mock_file_data
    
