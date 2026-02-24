"""Verify generated agent template counts."""

from pathlib import Path


def main() -> None:
    root = Path("agents_100")
    category_counts = {}
    total_agents = 0

    for category in sorted([p for p in root.iterdir() if p.is_dir()]):
        count = len(
            [
                f
                for f in category.glob("*.py")
                if f.name != "__init__.py"
            ]
        )
        category_counts[category.name] = count
        total_agents += count

    print("Total agent files:", total_agents)
    for name, count in category_counts.items():
        print(f"{name}: {count}")


if __name__ == "__main__":
    main()

