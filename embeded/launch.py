import argparse
import os
import subprocess


def generate_sketch(crop_dir: str):
    config_path = os.path.join(crop_dir, "config.json")
    command = [
        "python",
        "generate_sketch.py",
        "--output",
        crop_dir,
        "--config-path",
        config_path,
    ]
    print(f"[MAIN] Generating main.ino in: {crop_dir}")
    subprocess.run(command, check=True)


def upload_arduino(crop_dir: str):
    config_path = os.path.join(crop_dir, "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    com = config["com"]
    board = config["board"]
    sketch_path = os.path.join(crop_dir, "main")

    print(f"[LIB] Ensuring DHT libraries are installed...")
    subprocess.run(
        ["arduino-cli", "lib", "install", "DHT sensor library"], check=True
    )
    subprocess.run(
        ["arduino-cli", "lib", "install", "Adafruit Unified Sensor"], check=True
    )

    print(f"[UPLOAD] Compiling and uploading to {com} with board {board}")

    compile_cmd = ["arduino-cli", "compile", "--fqbn", board, sketch_path]
    upload_cmd = [
        "arduino-cli",
        "upload",
        "-p",
        com,
        "--fqbn",
        board,
        sketch_path,
    ]

    subprocess.run(compile_cmd, check=True)
    subprocess.run(upload_cmd, check=True)


def update_sensor(crop_dir: str):
    config_path = os.path.join(crop_dir, "config.json")
    command = [
        "python",
        "update_sensor.py",
        "--config-path",
        config_path,
    ]
    print(f"[SERIAL] Launching serial listener for: {crop_dir}")
    subprocess.Popen(command)


def main():
    parser = argparse.ArgumentParser(
        description="Generate, upload, and launch serial update for all crop_* dirs"
    )
    parser.add_argument(
        "--root", required=True, help="Root directory containing crop_* folders"
    )

    args = parser.parse_args()
    crop_dirs = [
        os.path.join(args.root, d)
        for d in os.listdir(args.root)
        if os.path.isdir(os.path.join(args.root, d)) and d.startswith("crop_")
    ]

    if not crop_dirs:
        print("[WARN] No crop_* directories found.")
        return

    for crop_dir in crop_dirs:
        print(f"\n=== Processing: {crop_dir} ===")
        generate_sketch(crop_dir)
        upload_arduino(crop_dir)
        update_sensor(crop_dir)


if __name__ == "__main__":
    import json  # 위치 중요 (upload_arduino 내부 사용)

    main()
