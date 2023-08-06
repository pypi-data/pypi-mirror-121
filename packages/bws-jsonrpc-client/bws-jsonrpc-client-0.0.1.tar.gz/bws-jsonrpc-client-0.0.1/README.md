# JsonRpcClient


```python

from jsonrpc_client import JsonRpcClient

api = JsonRpcClient("http://localhost:8181/rpc")

api.sum(1, 2)

api.module.get_test(name="jad21", type="B")

```