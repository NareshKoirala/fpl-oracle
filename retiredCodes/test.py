import json
import sys


def json_to_redis_pipe(json_filepath, output_filepath):
    try:
        with open(json_filepath, "r") as f:
            data = json.load(f)

        with open(output_filepath, "w") as out:
            # 1. Handle if JSON is a standard key-value dictionary
            if isinstance(data, dict):
                for key, value in data.items():
                    # Converts objects/lists to string format to store cleanly in Redis
                    val_str = (
                        json.dumps(value)
                        if isinstance(value, (dict, list))
                        else str(value)
                    )
                    out.write(f"SET {key} '{val_str}'\n")

            # 2. Handle if JSON is an array of rdbtools-style records
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "key" in item and "value" in item:
                        key = item["key"]
                        value = item["value"]
                        val_str = (
                            json.dumps(value)
                            if isinstance(value, (dict, list))
                            else str(value)
                        )
                        out.write(f"SET {key} '{val_str}'\n")
                    else:
                        print(
                            "Skipping unrecognized list item format.", file=sys.stderr
                        )

        print(f"Successfully generated protocol file: {output_filepath}")
    except Exception as e:
        print(f"Error processing files: {e}", file=sys.stderr)


if __name__ == "__main__":
    # Converts your test file into a text file full of standard raw Redis commands
    json_to_redis_pipe("test.json", "redis_commands.txt")
