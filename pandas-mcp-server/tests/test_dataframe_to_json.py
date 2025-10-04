import os
import json
import tempfile
import unittest
import pandas as pd
import numpy as np
from decimal import Decimal

import importlib.util
import os
import sys

# Ensure project root is on sys.path so `core` package imports resolve
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

# Inject lightweight stubs for core modules that server imports so tests can run
import types

core_config = types.SimpleNamespace(mcp=types.SimpleNamespace(tool=lambda *a, **k: (lambda f: f), run=lambda: None), BLACKLIST=[])
core_execution = types.SimpleNamespace(run_pandas_code=lambda code: {'result': None})
core_metadata = types.SimpleNamespace(read_metadata=lambda p: {})
core_visualization = types.SimpleNamespace(generate_chartjs=lambda *a, **k: {})

import sys
sys.modules['core'] = types.ModuleType('core')
sys.modules['core.config'] = types.ModuleType('core.config')
sys.modules['core.execution'] = types.ModuleType('core.execution')
sys.modules['core.metadata'] = types.ModuleType('core.metadata')
sys.modules['core.visualization'] = types.ModuleType('core.visualization')
sys.modules['core.config'].mcp = core_config.mcp
sys.modules['core.config'].BLACKLIST = []
sys.modules['core.execution'].run_pandas_code = core_execution.run_pandas_code
sys.modules['core.metadata'].read_metadata = core_metadata.read_metadata
sys.modules['core.visualization'].generate_chartjs = core_visualization.generate_chartjs

# Load server.py as a module by file path to avoid import issues during test execution
server_path = os.path.join(basedir, 'server.py')
spec = importlib.util.spec_from_file_location('server', server_path)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)



class DataFrameToJsonTest(unittest.TestCase):
    def test_dataframe_to_json_tool_serialization(self):
        # Create a sample DataFrame with various types
        df = pd.DataFrame({
            'int_col': [1, 2],
            'float_col': [1.5, 2.5],
            'np_int': np.array([3, 4], dtype=np.int64),
            'date_col': [pd.Timestamp('2020-01-01'), pd.Timestamp('2020-01-02')],
            'dec_col': [Decimal('1.23'), Decimal('4.56')],
            'none_col': [None, pd.NA]
        })

        # Monkeypatch run_pandas_code to return the DataFrame as result
        orig = getattr(server, 'run_pandas_code', None)

        def fake_run_pandas_code(code):
            return {'result': df}

        try:
            server.run_pandas_code = fake_run_pandas_code

            with tempfile.TemporaryDirectory() as td:
                out_file = os.path.join(td, 'out.json')
                res = server.dataframe_to_json_tool("fake code", out_file, orient='records')
                self.assertEqual(res['status'], 'SUCCESS')
                self.assertTrue(os.path.exists(out_file))

                data = json.loads(open(out_file, encoding='utf-8').read())
                # Should be a list of records
                self.assertIsInstance(data, list)
                self.assertEqual(data[0]['int_col'], 1)
                self.assertAlmostEqual(data[0]['float_col'], 1.5)
                self.assertTrue(str(data[0]['date_col']).startswith('2020-01-01'))
                self.assertEqual(data[0]['dec_col'], '1.23')
                self.assertIsNone(data[0]['none_col'])
        finally:
            if orig is not None:
                server.run_pandas_code = orig
            else:
                delattr(server, 'run_pandas_code')


if __name__ == '__main__':
    unittest.main()
