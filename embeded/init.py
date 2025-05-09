import argparse
import requests
import os
import json
import subprocess

API_BASE_URL = "http://3.26.202.82:8000/api"


def get_group_info(group_id: int):
    url = f"{API_BASE_URL}/group/{group_id}"
    res = requests.get(url, timeout=5)
    res.raise_for_status()
    return res.json()["data"]


def generate_config(crop_id: int, com: str, board: str, output_dir: str):
    command = [
        "python",
        "generate_config.py",
        "--crop-id",
        str(crop_id),
        "--com",
        com,
        "--board",
        board,
        "--output",
        output_dir,
    ]
    subprocess.run(command, check=True)


def generate_main_ino(config_path: str, output_dir: str):
    command = [
        "python",
        "generate_main_ino.py",
        "--config",
        config_path,
        "--output",
        output_dir,
    ]
    subprocess.run(command, check=True)


def upload_from_config(config_path: str):
    command = [
        "python",
        "generate_main_ino.py",  # 재사용
        "--config",
        config_path,
        "--output",
        os.path.dirname(config_path),
    ]
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Initialize all crops in a group (config-based)"
    )
    parser.add_argument("--group-id", required=True, type=int)
    parser.add_argument(
        "--com", required=True, help="Shared COM port for all crops"
    )
    parser.add_argument("--board", default="arduino:avr:uno", help="Board type")
    parser.add_argument("--output", required=True, help="Root output directory")
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Run upload after main.ino generation",
    )

    args = parser.parse_args()
    group = get_group_info(args.group_id)
    crops = group["crops"]

    for crop in crops:
        crop_id = crop["crop_id"]
        crop_dir = os.path.join(args.output, f"crop_{crop_id}")
        os.makedirs(crop_dir, exist_ok=True)

        print(f"\n=== Crop {crop_id} ===")

        config_path = os.path.join(crop_dir, "config.json")

        # Step 1: config.json 생성
        generate_config(crop_id, args.com, args.board, crop_dir)

        # Step 2: main.ino 생성
        generate_main_ino(config_path, crop_dir)

        # Step 3: 업로드
        if args.upload:
            upload_from_config(config_path)


if __name__ == "__main__":
    main()
