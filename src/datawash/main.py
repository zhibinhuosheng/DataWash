import argparse
import os

from .config.pipeline_config import PipelineConfig
from .pipeline.pipeline_builder import PipelineBuilder


def main():
    parser = argparse.ArgumentParser(description="DataWash - 语料清洗工具")
    parser.add_argument("--mode", required=True, choices=["testcase", "aw"], help="清洗模式: testcase 或 aw")
    parser.add_argument("--input", required=True, help="输入路径（testcase模式为目录，aw模式为JSON文件）")
    parser.add_argument("--output", required=True, help="输出目录")
    parser.add_argument("--source-root", required=True, help="源文件根目录")
    args = parser.parse_args()

    if args.mode == "testcase":
        input_paths = [args.input] if os.path.isfile(args.input) else [args.input]
    else:
        input_paths = [args.input]

    config = PipelineConfig(
        input_paths=input_paths,
        output_dir=args.output,
        source_root=args.source_root,
    )

    if args.mode == "testcase":
        pipeline = PipelineBuilder.build_test_case_pipeline(config)
    else:
        pipeline = PipelineBuilder.build_aw_pipeline(config)

    pipeline.run(config)
    print(f"清洗完成，输出目录: {args.output}")


if __name__ == "__main__":
    main()
