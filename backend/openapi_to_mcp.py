import yaml

def generate_mcp_tools(openapi_path):
    with open(openapi_path, "r") as f:
        spec = yaml.safe_load(f)

    tools = []
    for path, methods in spec["paths"].items():
        for method, meta in methods.items():
            tools.append({
                "name": f"{method}_{path.replace('/', '_')}",
                "description": meta.get("summary", ""),
                "input_schema": meta.get("requestBody", {}),
                "output_schema": meta.get("responses", {})
            })
    return tools
