from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
THEME_NAME = "Wiznote X"
THEME_FILES = {
    "obsidian": [
        ROOT_DIR / "theme.css",
        ROOT_DIR / "manifest.json",
    ],
}


def require_windows_appdata_dir(
    appdata_dir: Path | None,
    missing_message: str,
) -> Path:
    resolved_appdata_dir = appdata_dir or (
        Path(os.environ["APPDATA"]) if os.environ.get("APPDATA") else None
    )
    if resolved_appdata_dir is None:
        raise RuntimeError(missing_message)

    return resolved_appdata_dir


def detect_default_obsidian_config_dir(
    system_name: str | None = None,
    home_dir: Path | None = None,
    appdata_dir: Path | None = None,
) -> Path:
    resolved_system_name = system_name or platform.system()
    resolved_home_dir = home_dir or Path.home()

    if resolved_system_name == "Windows":
        return (
            require_windows_appdata_dir(
                appdata_dir,
                "APPDATA is not set; cannot locate Obsidian config.",
            )
            / "obsidian"
        )

    if resolved_system_name == "Darwin":
        return resolved_home_dir / "Library" / "Application Support" / "obsidian"

    return resolved_home_dir / ".config" / "obsidian"


def is_obsidian_vault_dir(candidate_dir: Path) -> bool:
    return (candidate_dir / ".obsidian").is_dir()


def load_json_object(json_file: Path, *, description: str) -> dict[str, object]:
    try:
        json_data = json.loads(json_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{description} is invalid JSON: {json_file}") from exc

    if not isinstance(json_data, dict):
        raise RuntimeError(f"{description} must be a JSON object: {json_file}")

    return json_data


def build_obsidian_theme_dir(vault_dir: Path) -> Path:
    return vault_dir / ".obsidian" / "themes" / THEME_NAME


def find_obsidian_vault_dir(start_dir: Path, *, required: bool) -> Path | None:
    resolved_start_dir = start_dir.expanduser().resolve()
    if not resolved_start_dir.exists() or not resolved_start_dir.is_dir():
        if required:
            raise RuntimeError(f"Vault directory does not exist: {resolved_start_dir}")
        return None

    for candidate_dir in (resolved_start_dir, *resolved_start_dir.parents):
        if is_obsidian_vault_dir(candidate_dir):
            return candidate_dir

    if required:
        raise RuntimeError(
            f"Vault does not contain a .obsidian directory: {resolved_start_dir}"
        )

    return None


def detect_configured_obsidian_vault_dirs(config_dir: Path) -> list[Path]:
    config_file = config_dir / "obsidian.json"
    if not config_file.exists():
        raise RuntimeError(f"Obsidian config file does not exist: {config_file}")

    config_data = load_json_object(config_file, description="Obsidian config")
    raw_vaults = config_data.get("vaults")
    if not isinstance(raw_vaults, dict) or not raw_vaults:
        raise RuntimeError(f"Obsidian config does not contain any vaults: {config_file}")

    sorted_vaults = sorted(
        raw_vaults.values(),
        key=lambda vault: (
            bool(vault.get("open")),
            int(vault.get("ts", 0)),
        ),
        reverse=True,
    )
    configured_vault_dirs: list[Path] = []
    for candidate_vault in sorted_vaults:
        raw_path = candidate_vault.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            continue

        candidate_dir = Path(raw_path).expanduser().resolve()
        if candidate_dir.is_dir() and is_obsidian_vault_dir(candidate_dir):
            configured_vault_dirs.append(candidate_dir)

    if not configured_vault_dirs:
        raise RuntimeError(
            "Obsidian config does not point to any accessible vaults with a .obsidian directory."
        )

    return configured_vault_dirs


def detect_default_obsidian_vault_dirs(
    start_dir: Path | None = None,
    config_dir: Path | None = None,
) -> list[Path]:
    detected_vault_dirs: list[Path] = []
    current_vault_dir = find_obsidian_vault_dir(start_dir or Path.cwd(), required=False)
    if current_vault_dir is not None:
        detected_vault_dirs.append(current_vault_dir)

    try:
        configured_vault_dirs = detect_configured_obsidian_vault_dirs(
            config_dir or detect_default_obsidian_config_dir()
        )
    except RuntimeError as exc:
        if not detected_vault_dirs:
            raise RuntimeError(
                "Could not detect any Obsidian vaults. "
                "Open a vault in Obsidian first, run this command from inside a vault, or pass --vault."
            ) from exc
        configured_vault_dirs = []

    for configured_vault_dir in configured_vault_dirs:
        if configured_vault_dir not in detected_vault_dirs:
            detected_vault_dirs.append(configured_vault_dir)

    return detected_vault_dirs


def resolve_obsidian_vault_dir(vault_dir: Path) -> Path:
    resolved_vault_dir = find_obsidian_vault_dir(vault_dir, required=True)
    if resolved_vault_dir is None:
        raise RuntimeError(f"Vault does not contain a .obsidian directory: {vault_dir}")
    return resolved_vault_dir


def resolve_obsidian_theme_dir(vault_dir: Path) -> Path:
    return build_obsidian_theme_dir(resolve_obsidian_vault_dir(vault_dir))


def activate_obsidian_theme(vault_dir: Path) -> None:
    appearance_file = (
        resolve_obsidian_vault_dir(vault_dir) / ".obsidian" / "appearance.json"
    )
    if appearance_file.exists():
        appearance_data = load_json_object(
            appearance_file,
            description="Obsidian appearance config",
        )
    else:
        appearance_data = {}

    appearance_data["cssTheme"] = THEME_NAME
    appearance_file.write_text(
        json.dumps(appearance_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def copy_theme_files(
    source_files: list[Path],
    target_dir: Path,
    force: bool = True,
) -> list[str]:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied_files: list[str] = []

    for source_file in source_files:
        if not source_file.exists():
            raise FileNotFoundError(f"Theme source file missing: {source_file}")

        destination = target_dir / source_file.name
        if destination.exists() and not force:
            raise FileExistsError(f"Destination already exists: {destination}")

        shutil.copy2(source_file, destination)
        copied_files.append(source_file.name)

    return copied_files


def install_theme_files(
    app_name: str,
    target_dir: Path,
    force: bool = True,
) -> list[str]:
    source_files = THEME_FILES.get(app_name)
    if source_files is None:
        raise RuntimeError(f"Unsupported app: {app_name}")

    return copy_theme_files(source_files, target_dir, force)


def install_obsidian_theme(
    vault_dir: Path,
    force: bool = True,
) -> tuple[Path, list[str]]:
    resolved_vault_dir = resolve_obsidian_vault_dir(vault_dir)
    target_dir = build_obsidian_theme_dir(resolved_vault_dir)
    copied_files = install_theme_files("obsidian", target_dir, force)
    activate_obsidian_theme(resolved_vault_dir)
    return target_dir, copied_files


def print_install_result(app_label: str, target_dir: Path, copied_files: list[str]) -> None:
    print(f"Installed {app_label} {THEME_NAME} theme to: {target_dir.resolve()}")
    print(f"Copied files: {', '.join(copied_files)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the Wiznote X theme for Obsidian from this repository."
    )
    subparsers = parser.add_subparsers(dest="app_name", required=True)

    obsidian_parser = subparsers.add_parser(
        "obsidian",
        help="Install the Wiznote X theme into one vault or all detected Obsidian vaults.",
    )
    obsidian_parser.add_argument(
        "--vault",
        type=Path,
        help="Install into a specific Obsidian vault instead of all detected vaults.",
    )
    obsidian_parser.add_argument(
        "--force",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Overwrite existing theme files if they already exist.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.app_name != "obsidian":
            raise RuntimeError(f"Unsupported app: {args.app_name}")

        if args.vault is not None:
            target_dir, copied_files = install_obsidian_theme(args.vault, args.force)
            print_install_result("Obsidian", target_dir, copied_files)
            return 0

        for vault_dir in detect_default_obsidian_vault_dirs():
            target_dir, copied_files = install_obsidian_theme(vault_dir, args.force)
            print_install_result("Obsidian", target_dir, copied_files)
        return 0
    except Exception as exc:  # pragma: no cover - exercised by CLI behavior tests
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
