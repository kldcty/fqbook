#!/usr/bin/env python3
"""打包脚本 - 将 mdBook 输出打包为 zip 归档

用法:
    python package.py
    uv run package.py
"""

from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path


def get_package_name() -> str:
    """生成打包文件名：fqbook-YYYY-mm-dd.zip"""
    today: datetime = datetime.now()
    return f"fqbook-{today.year:04d}-{today.month:02d}-{today.day:02d}.zip"


def create_zip(source_dir: Path, output_path: Path) -> None:
    """创建 zip 归档

    Args:
        source_dir: 要打包的源目录
        output_path: 输出 zip 文件路径
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in source_dir.rglob("*"):
            if file.is_file():
                # 计算相对路径，保持目录结构
                arcname = file.relative_to(source_dir.parent)
                zf.write(file, arcname)


def main() -> None:
    """主函数"""
    # 定义路径
    root_dir: Path = Path(__file__).parent
    book_dir: Path = root_dir / "book"
    output_path: Path = root_dir / get_package_name()

    # 检查 book 目录是否存在
    if not book_dir.exists():
        raise FileNotFoundError(f"未找到编译输出目录: {book_dir}")

    # 删除旧的打包文件（如果存在）
    if output_path.exists():
        print(f"删除旧文件: {output_path.name}")
        output_path.unlink()

    # 创建 zip
    print(f"正在打包: {book_dir} -> {output_path.name}")
    create_zip(book_dir, output_path)

    # 显示文件大小
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"打包完成: {output_path.name} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
