import argparse
import subprocess

def parse_pipeline_args() -> argparse.Namespace:
    """Parse arguments for the master pipeline runner."""
    parser = argparse.ArgumentParser(description="Run the full NLP pipeline.")
    parser.add_argument("--band", type=str, required=True, help="Band name.")
    parser.add_argument("--songs", type=int, default=50, help="Max songs.")
    parser.add_argument("--topics", type=int, default=5, help="Num topics.")
    return parser.parse_args()

def run_command(command: list[str]) -> None:
    """Execute a shell command via subprocess."""
    print(f"\n--- Running: {' '.join(command)} ---")
    subprocess.run(command, check=True)

def main() -> None:
    """Execute all project stages sequentially."""
    args = parse_pipeline_args()
    band = args.band
    
    run_command(["python", "-m", "src.collect", "--band", band, "--max_songs", str(args.songs)])
    run_command(["python", "-m", "src.process", "--band", band])
    run_command(["python", "-m", "src.analyze", "--band", band, "--topics", str(args.topics)])
    run_command(["python", "-m", "src.build_graph", "--band", band])
    
    print(f"\n✅ Pipeline complete for '{band}'! Ready for visualization.")

if __name__ == "__main__":
    main()