import os

from datawash.config.pipeline_config import PipelineConfig
from datawash.pipeline.pipeline_builder import PipelineBuilder


def main():
    input_path = os.environ.get("DATAWASH_INPUT", "")
    output_dir = os.environ.get("DATAWASH_OUTPUT", "")
    source_root = os.environ.get("DATAWASH_SOURCE_ROOT", "")

    if not all([input_path, output_dir, source_root]):
        print("用法: python -m datawash.testcase_wash --input <路径> --output <目录> --source-root <根目录>")
        return

    config = PipelineConfig(
        input_paths=[input_path] if os.path.isfile(input_path) else [input_path],
        output_dir=output_dir,
        source_root=source_root,
    )

    pipeline = PipelineBuilder.build_test_case_pipeline(config)
    pipeline.run(config)
    print(f"测试用例清洗完成，输出目录: {output_dir}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="测试用例语料清洗")
    parser.add_argument("--input", required=True, help="输入路径")
    parser.add_argument("--output", required=True, help="输出目录")
    parser.add_argument("--source-root", required=True, help="源文件根目录")
    args = parser.parse_args()

    config = PipelineConfig(
        input_paths=[args.input] if os.path.isfile(args.input) else [args.input],
        output_dir=args.output,
        source_root=args.source_root,
    )

    pipeline = PipelineBuilder.build_test_case_pipeline(config)
    pipeline.run(config)
    print(f"测试用例清洗完成，输出目录: {args.output}")
